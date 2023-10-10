from base_count import BaseCount
import statistics as stat
import random as rand


rand.seed(10)

class CountMin(BaseCount):
    def __init__(self, R=1):
        super().__init__(R)

    def increment(self, token):
        self.try_heap(token, self.estimate(token))

        for i in range(self.d):
            hRes = self.hashFuncs[i](token)
            self.count[i][hRes] += 1

    def estimate(self, token):
        res = float('inf')
        for i in range(self.d):
            hRes = self.hashFuncs[i](token)
            res = min(res, self.count[i][hRes])

        return res


class CountMed(BaseCount):
    def __init__(self, R=1):
        super().__init__(R)

    def increment(self, token):
        self.try_heap(token, self.estimate(token))

        for i in range(self.d):
            hRes = self.hashFuncs[i](token)
            self.count[i][hRes] += 1

    def estimate(self, token):
        res = []
        for i in range(self.d):
            hRes = self.hashFuncs[i](token)
            res.append(self.count[i][hRes])

        return stat.median(res)
    

class CountSketch(BaseCount):
    def __init__(self, R=1):
        super().__init__(R)

    def increment(self, token):
        self.try_heap(token, self.estimate(token))
        
        for i in range(self.d):
            hRes = self.hashFuncs[i](token)
            s = 1 if rand.randint(0, 1) == 1 else -1
            self.count[i][hRes] += s

    def estimate(self, token):
        res = []
        for i in range(self.d):
            hRes = self.hashFuncs[i](token)
            s = 1 if rand.randint(0, 1) == 1 else -1
            res.append(self.count[i][hRes] * s)

        return stat.median(res)
    




