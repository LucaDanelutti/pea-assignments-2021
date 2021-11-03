import random
import math

def compute(total_t):
    # Generate exponential distributed trace
    def compute_exponential(n, l):
        exponential = []
        def gen_exp():
            return - math.log(random.random()) / l
        for i in range(0, n):
            exponential.append(gen_exp())
        return exponential

    # Generate erlang distributed trace
    def compute_erlang(n, l, k):
        erlang = []
        def gen_erlang():
            res = 0
            for i in range(0, k):
                res -= (math.log(random.random())/l)
            return res
        for i in range(0, n):
            erlang.append(gen_erlang())
        return erlang

    # State machine variables
    s = 1
    t = 0
    # Partial times
    ts0 = 0
    ts1 = 0
    ts2 = 0
    # State machine logic
    while t<total_t:
        # 0: shop is empty waiting for customers
        if s==0:
            ns = 1
            ds = compute_exponential(1, 0.005)[0]
            ts0 += ds
        # 1: a customer enters the shop
        if s==1:
            rand = random.random()
            if rand < 0.8:
                ns = 2
            else:
                rand2 = random.random()
                if rand2 < 0.5:
                    ns = 0
                else:
                    ns = 1
            ds = compute_erlang(1, 0.1, 3)[0]
            ts1 += ds
        # 2: customer accepted -> service stage
        if s==2:
            rand = random.random()
            if rand < 0.5:
                ns = 0
            else:
                ns = 1
            ds = compute_exponential(1, 0.01)[0]
            ts2 += ds
        s = ns
        t += ds
    print("Probability of having a customer in the first stage: %f" % (ts1/total_t))
    print("Probability of having a customer in the second stage: %f" % (ts2/total_t))
    print("Probability of having the shop empty: %f" % (ts0/total_t))
    print("Utilization: %f" % (1 - ts0 / total_t))

def run():
    compute(1000000)

if __name__ == '__main__':
    run()
