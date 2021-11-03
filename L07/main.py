import random
import math

def compute(total_t, d_confidence, k):
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

    def state_machine(total_t):
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
        return ts0, ts1, ts2
    ts0, ts1, ts2 = state_machine(total_t)
    print("Probability of having a customer in the first stage: %f" % (ts1/total_t))
    print("Probability of having a customer in the second stage: %f" % (ts2/total_t))
    print("Probability of having the shop empty: %f" % (ts0/total_t))
    print("Utilization: %f" % (1 - ts0 / total_t))

    # Compute confidence interval
    def compute_confidence_interval(name, ps, d_confidence, k):
        values = []
        for i in range(0, k):
            values.append(ps[i])
        # Compute x
        cumul = 0
        for i in range(0, k):
            cumul += values[i]
        x = 1 / k * cumul
        # Compute s_square
        cumul = 0
        for i in range(0, k):
            cumul += (values[i] - x) * (values[i] - x)
        s_square = 1 / (k-1) * cumul

        print("Confidence interval of %s: [%f, %f]" % (name, x - d_confidence * math.pow(
            s_square / k, 0.5), x + d_confidence * math.pow(s_square / k, 0.5)))
    
    # Compute k probabilities
    p0s, p1s, p2s = [], [], []
    us = []
    for i in range(0, k):
        ts0, ts1, ts2 = state_machine(total_t)
        p0s.append(ts0/total_t)
        p1s.append(ts1/total_t)
        p2s.append(ts2/total_t)
        us.append(1 - ts0 / total_t)
    
    # Compute confidence intervals of probabilities
    compute_confidence_interval("empty shop", p0s, d_confidence, k)
    compute_confidence_interval("first stage", p1s, d_confidence, k)
    compute_confidence_interval("second stage", p2s, d_confidence, k)
    compute_confidence_interval("utilization", us, d_confidence, k)

    # Compute avgs
    print("Empty shop avg: %f" % (sum(p0s) / k))
    print("First stage avg: %f" % (sum(p1s) / k))
    print("Second stage avg: %f" % (sum(p2s) / k))
    print("Utilization avg: %f" % (sum(us) / k))

def run():
    compute(1000000, 1.96, 200)

if __name__ == '__main__':
    run()
