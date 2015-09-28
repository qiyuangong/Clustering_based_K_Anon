import unittest

from clustering_based_k_anon import clustering_kmember
import random

gl_K = 10
gl_rounds = 3
gl_QI_len = 5
gl_QI_range = [10, 10, 10, 10, 10]
# Build a GenTree object
gl_tree_temp = {}
tree = GenTree('*')
gl_tree_temp['*'] = tree
lt = GenTree('1,5', tree)
gl_tree_temp['1,5'] = lt
rt = GenTree('6,10', tree)
gl_tree_temp['6,10'] = rt
for i in range(1, 11):
    if i <= 5:
        t = GenTree(str(i), lt, True)
    else:
        t = GenTree(str(i), rt, True)
    gl_tree_temp[str(i)] = t


if __name__ == '__main__':
    unittest.main()
