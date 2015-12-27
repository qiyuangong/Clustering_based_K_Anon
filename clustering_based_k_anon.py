"""
main module for cluster_based_k_anon
"""
#!/usr/bin/env python
#coding=utf-8

from models.numrange import NumRange
from models.gentree import GenTree
from utils.utility import get_num_list_from_str, cmp_str
import random
import time
import operator
import pdb


__DEBUG = False
# att_tree store root node for each att
ATT_TREES = []
# databack store all reacord for dataset
LEN_DATA = 0
QI_LEN = 0
QI_RANGE = []
IS_CAT = []


class Cluster(object):

    """Cluster is for cluster based k-anonymity
    middle denote generlized value for one cluster
    self.member: record list in cluster
    self.middle: middle node in cluster
    """

    def __init__(self, member, middle):
        self.iloss = 0.0
        self.member = member
        self.middle = middle[:]

    def add_record(self, record):
        """
        add record to cluster
        """
        self.member.append(record)
        self.middle = middle(self.middle, record)

    def merge_group(self, group, middle):
        """merge group into self_gourp and delete group elements.
        update self.middle with middle
        """
        while group.member:
            temp = group.member.pop()
            self.member.append(temp)
        self.middle = middle[:]

    def merge_record(self, record, middle):
        """merge record into hostgourp. update self.middle with middle
        """
        self.member.append(record)
        self.middle = middle[:]

    def __len__(self):
        """
        return number of records in cluster
        """
        return len(self.member)


def r_distance(source, target):
    """
    Return distance between source (cluster or record)
    and target (cluster or record). The distance is based on
    NCP (Normalized Certainty Penalty) on relational part.
    If source or target are cluster, func need to multiply
    source_len (or target_len).
    """
    source_mid = source
    target_mid = target
    source_len = 1
    target_len = 1
    # check if target is Cluster
    if isinstance(target, Cluster):
        target_mid = target.middle
        target_len = len(target)
    # check if souce is Cluster
    if isinstance(source, Cluster):
        source_mid = source.middle
        source_len = len(source)
    if source_mid == target_mid:
        return 0
    mid = middle(source_mid, target_mid)
    # len should be taken into account
    distance = (source_len + target_len) * NCP(mid)
    return distance


def diff_distance(record, cluster):
    """
    Return distance between record
    and cluster. The distance is based on increasement of
    NCP (Normalized Certainty Penalty) on relational part.
    """
    mid = cluster.middle
    len_cluster = len(cluster)
    mid_after = middle(record, mid)
    return NCP(mid_after) * (len_cluster + 1) - NCP(mid) * len_cluster


def NCP(mid):
    """Compute NCP (Normalized Certainty Penalty)
    when generate record to middle.
    """
    ncp = 0.0
    # exclude SA values(last one type [])
    for i in range(QI_LEN):
        # if leaf_num of numerator is 1, then NCP is 0
        width = 0.0
        if IS_CAT[i] is False:
            try:
                float(mid[i])
            except ValueError:
                temp = mid[i].split(',')
                width = float(temp[1]) - float(temp[0])
        else:
            width = len(ATT_TREES[i][mid[i]]) * 1.0
        width /= QI_RANGE[i]
        ncp += width
    return ncp


def get_LCA(index, item1, item2):
    """Get lowest commmon ancestor (including themselves)"""
    # get parent list from
    if item1 == item2:
        return item1
    parent1 = ATT_TREES[index][item1].parent[:]
    parent2 = ATT_TREES[index][item2].parent[:]
    parent1.insert(0, ATT_TREES[index][item1])
    parent2.insert(0, ATT_TREES[index][item2])
    minlen = min(len(parent1), len(parent2))
    last_LCA = parent1[-1]
    # note here: when trying to access list reversely, take care of -0
    for i in range(1, minlen + 1):
        if parent1[-i].value == parent2[-i].value:
            last_LCA = parent1[-i]
        else:
            break
    return last_LCA.value


def middle(record1, record2):
    """
    Compute relational generalization result of record1 and record2
    """
    mid = []
    for i in range(QI_LEN):
        if IS_CAT[i] is False:
            split_number = []
            split_number.extend(get_num_list_from_str(record1[i]))
            split_number.extend(get_num_list_from_str(record2[i]))
            split_number.sort(cmp=cmp_str)
            if split_number[0] == split_number[-1]:
                mid.append(split_number[0])
            else:
                mid.append(split_number[0] + ',' + split_number[-1])
        else:
            mid.append(get_LCA(i, record1[i], record2[i]))
    return mid


def middle_for_cluster(records):
    """
    calculat middle of records(list) recursively.
    Compute both relational middle for records (list).
    """
    len_r = len(records)
    mid = records[0]
    for i in range(1, len_r):
        mid = middle(mid, records[i])
    return mid


def find_best_knn(index, k, data):
    """key fuction of KNN. Find k nearest neighbors of record, remove them from data"""
    dist_dict = {}
    record = data[index]
    max_distance = 1000000000000
    # add random seed to cluster
    for i, t in enumerate(data):
        if i == index:
            continue
        dist = r_distance(record, t)
        dist_dict[i] = dist
    sorted_dict = sorted(dist_dict.iteritems(), key=operator.itemgetter(1))
    knn = sorted_dict[:k - 1]
    knn.append((index, 0))
    record_index = [t[0] for t in knn]
    elements = [data[t[0]] for t in knn]
    cluster = Cluster(elements, middle_for_cluster(elements))
    # delete multiple elements from data according to knn index list
    return cluster, record_index


def find_best_cluster_knn(record, clusters):
    """residual assignment. Find best cluster for record."""
    min_distance = 1000000000000
    min_index = 0
    best_cluster = clusters[0]
    for i, t in enumerate(clusters):
        distance = r_distance(record, t.middle)
        if distance < min_distance:
            min_distance = distance
            min_index = i
            best_cluster = t
    # add record to best cluster
    return min_index


def clustering_knn(data, k=25):
    """
    Group record according to QID distance. KNN
    """
    clusters = []
    # randomly choose seed and find k-1 nearest records to form cluster with size k
    while len(data) >= k:
        index = random.randrange(len(data))
        cluster, record_index = find_best_knn(index, k, data)
        data = [t for i, t in enumerate(data[:]) if i not in set(record_index)]
        clusters.append(cluster)
    # residual assignment
    while len(data) > 0:
        t = data.pop()
        cluster_index = find_best_cluster_knn(t, clusters)
        clusters[cluster_index].add_record(t)
    return clusters


def find_best_cluster_kmember(record, clusters):
    """residual assignment. Find best cluster for record."""
    min_diff = 1000000000000
    min_index = 0
    best_cluster = clusters[0]
    for i, t in enumerate(clusters):
        IF_diff = diff_distance(record, t)
        if IF_diff < min_diff:
            min_distance = IF_diff
            min_index = i
            best_cluster = t
    # add record to best cluster
    return min_index


def find_furthest_record(record, data):
    """
    :param record: the latest record be added to cluster
    :param data: remain records in data
    :return: the index of the furthest record from r_index
    """
    max_distance = 0
    max_index = -1
    for index in range(len(data)):
        current_distance = r_distance(record, data[index])
        if current_distance >= max_distance:
            max_distance = current_distance
            max_index = index
    return max_index


def find_best_record(cluster, data):
    """
    :param cluster: current
    :param data: remain dataset
    :return: index of record with min diff on information loss
    """
    # pdb.set_trace()
    min_diff = 1000000000000
    min_index = 0
    for index, record in enumerate(data):
        IF_diff = diff_distance(record, cluster)
        if IF_diff < min_diff:
            min_diff = IF_diff
            min_index = index
    return min_index


def clustering_kmember(data, k=25):
    """
    Group record according to NCP. K-member
    """
    clusters = []
    # randomly choose seed and find k-1 nearest records to form cluster with size k
    r_pos = random.randrange(len(data))
    record = data[r_pos]
    while len(data) >= k:
        r_pos = find_furthest_record(record, data)
        record = data.pop(r_pos)
        cluster = Cluster([record], record)
        while len(cluster) < k:
            r_pos = find_best_record(cluster, data)
            record = data.pop(r_pos)
            cluster.add_record(record)
        clusters.append(cluster)
        # pdb.set_trace()
    # residual assignment
    while len(data) > 0:
        t = data.pop()
        cluster_index = find_best_cluster_kmember(t, clusters)
        clusters[cluster_index].add_record(t)
    return clusters


def init(att_trees, data, QI_num=-1):
    """
    init global variables
    """
    global ATT_TREES, DATA_BACKUP, LEN_DATA, QI_RANGE, IS_CAT, QI_LEN
    ATT_TREES = att_trees
    QI_RANGE = []
    IS_CAT = []
    LEN_DATA = len(data)
    if QI_num <= 0:
        QI_LEN = len(data[0]) - 1
    else:
        QI_LEN = QI_num
    for i in range(QI_LEN):
        if isinstance(ATT_TREES[i], NumRange):
            IS_CAT.append(False)
            QI_RANGE.append(ATT_TREES[i].range)
        else:
            IS_CAT.append(True)
            QI_RANGE.append(len(ATT_TREES[i]['*']))


def clustering_based_k_anon(att_trees, data, type_alg='knn', k=10, QI_num=-1):
    """
    the main function of clustering based k-anon
    """
    init(att_trees, data, QI_num)
    result = []
    start_time = time.time()
    if type_alg == 'knn':
        print "Begin to KNN Cluster based on NCP"
        clusters = clustering_knn(data, k)
    elif type_alg == 'kmember':
        print "Begin to K-Member Cluster based on NCP"
        clusters = clustering_kmember(data, k)
    else:
        print "Please choose merge algorithm types"
        print "knn | kmember"
        return (0, (0, 0))
    rtime = float(time.time() - start_time)
    ncp = 0.0
    for cluster in clusters:
        gen_result = []
        mid = cluster.middle
        for i in range(len(cluster)):
            gen_result.append(mid)
        result.extend(gen_result)
        rncp = NCP(mid)
        ncp += 1.0 * rncp * len(cluster)
    ncp /= LEN_DATA
    ncp /= QI_LEN
    ncp *= 100
    if __DEBUG:
        print "NCP=", ncp
    return (result, (ncp, rtime))
