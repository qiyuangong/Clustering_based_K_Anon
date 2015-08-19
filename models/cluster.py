"""
class for clustering
"""

#!/usr/bin/env python
#coding=utf-8

# cluster for relational clusting


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
