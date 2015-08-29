"""
run cluster_based_k_anon with given parameters
"""

# !/usr/bin/env python
# coding=utf-8
from cluster_based_k_anon import cluster_based_k_anon
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
TYPE_ALG = 'knn'


def get_result_one(att_trees, data, type_alg, k=10):
    """
    run cluster_based_k_anon for one time, with k=10
    """
    print "K=%d" % k
    data_back = copy.deepcopy(data)
    _, eval_result = cluster_based_k_anon(att_trees, data, type_alg, k)
    data = copy.deepcopy(data_back)
    print "NCP %0.2f" % eval_result[0] + "%"
    print "Running time %0.2f" % eval_result[1] + " seconds"


def get_result_k(att_trees, data, type_alg):
    """
    change k, whle fixing QD and size of dataset
    """
    data_back = copy.deepcopy(data)
    for k in range(5, 55, 5):
        print '#' * 30
        print "K=%d" % k
        result, eval_result = cluster_based_k_anon(att_trees, data, type_alg, k)
        data = copy.deepcopy(data_back)
        print "NCP %0.2f" % eval_result[0] + "%"
        print "Running time %0.2f" % eval_result[1] + " seconds"


def get_result_dataset(att_trees, data, type_alg, k=10, num_test=10):
    """
    fix k and QI, while changing size of dataset
    num_test is the test nubmber.
    """
    data_back = copy.deepcopy(data)
    length = len(data_back)
    joint = 5000
    dataset_num = length / joint
    print "K=%d" % k
    if length % joint == 0:
        dataset_num += 1
    for i in range(1, dataset_num + 1):
        pos = i * joint
        ncp = rtime = 0
        if pos > length:
            continue
        print '#' * 30
        print "size of dataset %d" % pos
        for j in range(num_test):
            temp = random.sample(data, pos)
            _, eval_result = cluster_based_k_anon(att_trees, temp, type_alg, k)
            ncp += eval_result[0]
            rtime += eval_result[1]
            data = copy.deepcopy(data_back)
        ncp /= num_test
        rtime /= num_test
        print "Average NCP %0.2f" % ncp + "%"
        print "Running time %0.2f" % rtime + " seconds"
        print '#' * 30


def get_result_qi(att_trees, data, type_alg, k=5):
    """
    change nubmber of QI, whle fixing k and size of dataset
    """
    data_back = copy.deepcopy(data)
    num_data = len(data[0])
    print "L=%d" % k
    for i in reversed(range(1, num_data)):
        print '#' * 30
        print "Number of QI=%d" % i
        _, eval_result = cluster_based_k_anon(att_trees, data, type_alg, k, i)
        data = copy.deepcopy(data_back)
        print "NCP %0.2f" % eval_result[0] + "%"
        print "Running time %0.2f" % eval_result[1] + " seconds"


if __name__ == '__main__':
    FLAG = ''
    LEN_ARGV = len(sys.argv)
    try:
        TYPE_ALG = sys.argv[1]
        DATA_SELECT = sys.argv[2]
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
    DATA = DATA[:2000]
    if FLAG == 'k':
        get_result_k(ATT_TREES, DATA, TYPE_ALG)
    elif FLAG == 'qi':
        get_result_qi(ATT_TREES, DATA, TYPE_ALG)
    elif FLAG == 'data':
        get_result_dataset(ATT_TREES, DATA, TYPE_ALG)
    elif FLAG == '':
        # cProfile.run('get_result_one(ATT_TREES, DATA, TYPE_ALG)')
        get_result_one(ATT_TREES, DATA, TYPE_ALG)
    else:
        try:
            INPUT_K = int(FLAG)
            get_result_one(ATT_TREES, DATA, TYPE_ALG, INPUT_K)
        except ValueError:
            print "Usage: python anonymizer [knn | kmeber] [a | i] [k | qi | data]"
            print "a: adult dataset, i: INFORMS ataset"
            print "k: varying k"
            print "qi: varying qi numbers"
            print "data: varying size of dataset"
            print "example: python anonymizer a 5"
            print "example: python anonymizer a k"
    # anonymized dataset is stored in result
    print "Finish Cluster based K-Anon!!"
