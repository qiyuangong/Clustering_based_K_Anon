"""
run clustering_based_k_anon with given parameters
"""

# !/usr/bin/env python
# coding=utf-8
from clustering_based_k_anon import clustering_based_k_anon
from utils.read_adult_data import read_data as read_adult
from utils.read_adult_data import read_tree as read_adult_tree
from utils.read_informs_data import read_data as read_informs
from utils.read_informs_data import read_tree as read_informs_tree
import sys
import copy
import pdb
import random
import cProfile

DATA_SELECT = 'a'
TYPE_ALG = 'kmember'
DEFAULT_K = 10
__DEBUG = True


def extend_result(val):
    """
    separated with ',' if it is a list
    """
    if isinstance(val, list):
        return ','.join(val)
    return val


def write_to_file(result):
    """
    write the anonymized result to anonymized.data
    """
    with open("data/anonymized.data", "w") as output:
        for r in result:
            output.write(';'.join(map(extend_result, r)) + '\n')


def get_result_one(att_trees, data, type_alg, k=DEFAULT_K):
    "run clustering_based_k_anon for one time, with k=10"
    print "K=%d" % k
    data_back = copy.deepcopy(data)
    result, eval_result = clustering_based_k_anon(att_trees, data, type_alg, k)
    write_to_file(result)
    data = copy.deepcopy(data_back)
    print "NCP %0.2f" % eval_result[0] + "%"
    print "Running time %0.2f" % eval_result[1] + "seconds"


def get_result_n(att_trees, data, type_alg, k=DEFAULT_K, n=10):
    """
    run clustering_based_k_anon for n time, with k=10
    """
    print "K=%d" % k
    data_back = copy.deepcopy(data)
    n_ncp = 0.0
    n_time = 0.0
    for i in range(n):
        _, eval_result = clustering_based_k_anon(att_trees, data, type_alg, k)
        data = copy.deepcopy(data_back)
        n_ncp += eval_result[0]
        n_time += eval_result[1]
    n_ncp = n_ncp / n
    n_time = n_ncp / n
    print "Run %d times" % n
    print "NCP %0.2f" % n_ncp + "%"
    print "Running time %0.2f" % n_time + " seconds"


def get_result_k(att_trees, data, type_alg):
    """
    change k, whle fixing QD and size of dataset
    """
    data_back = copy.deepcopy(data)
    all_ncp = []
    all_rtime = []
    # for k in range(5, 105, 5):
    for k in [2, 5, 10, 25, 50, 100]:
        print '#' * 30
        print "K=%d" % k
        _, eval_result = clustering_based_k_anon(att_trees, data, type_alg, k)
        data = copy.deepcopy(data_back)
        print "NCP %0.2f" % eval_result[0] + "%"
        all_ncp.append(round(eval_result[0], 2))
        print "Running time %0.2f" % eval_result[1] + "seconds"
        all_rtime.append(round(eval_result[1], 2))
    print "All NCP", all_ncp
    print "All Running time", all_rtime


def get_result_dataset(att_trees, data, type_alg, k=DEFAULT_K, n=10):
    """
    fix k and QI, while changing size of dataset
    n is the proportion nubmber.
    """
    data_back = copy.deepcopy(data)
    length = len(data_back)
    print "K=%d" % k
    joint = 5000
    datasets = []
    check_time = length / joint
    if length % joint == 0:
        check_time -= 1
    for i in range(check_time):
        datasets.append(joint * (i + 1))
    datasets.append(length)
    all_ncp = []
    all_rtime = []
    for pos in datasets:
        ncp = rtime = 0
        print '#' * 30
        print "size of dataset %d" % pos
        for j in range(n):
            temp = random.sample(data, pos)
            _, eval_result = clustering_based_k_anon(att_trees,
                                                     temp, type_alg, k)
            ncp += eval_result[0]
            rtime += eval_result[1]
            data = copy.deepcopy(data_back)
        ncp /= n
        rtime /= n
        print "Average NCP %0.2f" % ncp + "%"
        all_ncp.append(round(ncp, 2))
        print "Running time %0.2f" % rtime + "seconds"
        all_rtime.append(round(rtime, 2))
    print '#' * 30
    print "All NCP", all_ncp
    print "All Running time", all_rtime


def get_result_qi(att_trees, data, type_alg, k=DEFAULT_K):
    """
    change nubmber of QI, whle fixing k and size of dataset
    """
    data_back = copy.deepcopy(data)
    ls = len(data[0])
    all_ncp = []
    all_rtime = []
    for i in range(1, ls):
        print '#' * 30
        print "Number of QI=%d" % i
        _, eval_result = clustering_based_k_anon(att_trees,
                                                 data, type_alg, k, i)
        data = copy.deepcopy(data_back)
        print "NCP %0.2f" % eval_result[0] + "%"
        all_ncp.append(round(eval_result[0], 2))
        print "Running time %0.2f" % eval_result[1] + "seconds"
        all_rtime.append(round(eval_result[1], 2))
    print "All NCP", all_ncp
    print "All Running time", all_rtime


if __name__ == '__main__':
    FLAG = ''
    LEN_ARGV = len(sys.argv)
    try:
        DATA_SELECT = sys.argv[1]
        TYPE_ALG = sys.argv[2]
        FLAG = sys.argv[3]
    except IndexError:
        pass
    INPUT_K = 5
    # read record
    if DATA_SELECT == 'i':
        print "INFORMS data"
        DATA = read_informs()
        ATT_TREES = read_informs_tree()
    else:
        print "Adult data"
        DATA = read_adult()
        ATT_TREES = read_adult_tree()
    if __DEBUG:
        # DATA = DATA[:2000]
        # print "Test anonymization with %d records" % len(DATA)
        print sys.argv
    if FLAG == 'k':
        get_result_k(ATT_TREES, DATA, TYPE_ALG)
    elif FLAG == 'qi':
        get_result_qi(ATT_TREES, DATA, TYPE_ALG)
    elif FLAG == 'data':
        get_result_dataset(ATT_TREES, DATA, TYPE_ALG)
    elif FLAG == 'n':
        get_result_n(ATT_TREES, DATA, TYPE_ALG)
    elif FLAG == '':
        if __DEBUG:
            cProfile.run('get_result_one(ATT_TREES, DATA, TYPE_ALG)')
        else:
            get_result_one(ATT_TREES, DATA, TYPE_ALG)
    else:
        try:
            INPUT_K = int(FLAG)
            get_result_one(ATT_TREES, DATA, TYPE_ALG, INPUT_K)
        except ValueError:
            print "Usage: python anonymizer [a | i] [knn | kmember | oka] [k | qi | data| n]"
            print "a: adult dataset, i: INFORMS ataset"
            print "knn: k-nearest neighborhood, kmember: k-member, oka: one time pass k-means"
            print "k: varying k"
            print "qi: varying qi numbers"
            print "data: varying size of dataset"
            print "example: python anonymizer a knn 5"
            print "example: python anonymizer a kmember k"
    # anonymized dataset is stored in result
    print "Finish Cluster based K-Anon!!"
