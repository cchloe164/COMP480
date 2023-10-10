import numpy as np
from sklearn.utils import murmurhash3_32
import random as rand
from heapq import heapify, heappush, heappop, heapreplace
import pandas as pd


class BaseCount():
    def __init__(self, R=1):
        self.d = 5
        self.R = R
        self.count = np.zeros((self.d, self.R), dtype=int)
        self.hashFuncs = [
            self.hash1,
            self.hash2,
            self.hash3,
            self.hash4,
            self.hash5,
        ]
        self.heap = []
        heapify(self.heap)
    
    def hash1(self, x):
        rand.seed(1)
        return murmurhash3_32(x) % self.R
    
    def hash2(self, x):
        rand.seed(2)
        return murmurhash3_32(x) % self.R
    
    def hash3(self, x):
        rand.seed(3)
        return murmurhash3_32(x) % self.R
    
    def hash4(self, x):
        rand.seed(4)
        return murmurhash3_32(x) % self.R
    
    def hash5(self, x):
        rand.seed(5)
        return murmurhash3_32(x) % self.R
    
    ############# HEAP FUNCTIONS ####################################
    def try_heap(self, token, est):
        if len(self.heap) < 500:    # populate empty heap
            heappush(self.heap, tuple([est, token]))
        else:   # heap is full
            if est > self.heap[0][0]:  # more popular token is found
                matches = [i for i, item in enumerate(self.heap) if item[1] == token]
                if matches == []:    # add new token and dump min token
                    heapreplace(self.heap, tuple([est, token]))
                    # heappop(self.heap)

                else:   # update existing token
                    self.heap[matches[0]] = tuple([est, token])

    def print_heap(self):
        return '\n'.join([(item[1] + ' ' + str(item[0])) for item in self.heap]) + '\n'
    
    def token_list_to_set(self):
        return set([item[1] for item in self.heap])
