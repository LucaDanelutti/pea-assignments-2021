import random
import math

def compute(total_t, d_confidence, k):
    # Generate exponential distributed trace
    def compute_exponential(l):
        def gen_exp():
            return - math.log(random.random()) / l
        exponential = gen_exp()
        return exponential

    def state_machine(total_t):
        # State machine variables
        s = 1
        t = 0
        # State machine counters
        ts0 = 0
        ts1 = 0
        ts2 = 0
        reports = 0
        # State machine logic
        while t<total_t:
            # 0: Normal operation
            if s==0:
                reporting = compute_exponential(0.05)
                maintenance = compute_exponential(0.001)
                if (reporting < maintenance):
                    ds = reporting
                    ns = 1
                else:
                    ds = maintenance
                    ns = 2
                ts0 += ds
            # 1: Reporting
            if s==1:
                normal = compute_exponential(1)
                maintenance = compute_exponential(0.001)
                if (normal < maintenance):
                    ds = normal
                    ns = 0
                else:
                    ds = maintenance
                    ns = 2
                ts1 += ds
                reports += 1
            # 2: Maintenance
            if s==2:
                ns = 0
                ds = compute_exponential(0.05)
                ts2 += ds
            s = ns
            t += ds
        return ts0, ts1, ts2, reports
    ts0, ts1, ts2, reports = state_machine(total_t)
    print("Probability of normal operation: %f" % (ts0/total_t))
    print("Probability of reporting: %f" %(ts1/total_t))
    print("Probability of maintenance: %f" % (ts2/total_t))
    print("Reporting frequency: %f" % (reports / total_t))

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
    rfs = []
    for i in range(0, k):
        ts0, ts1, ts2, reports = state_machine(total_t)
        p0s.append(ts0/total_t)
        p1s.append(ts1/total_t)
        p2s.append(ts2/total_t)
        rfs.append(reports / total_t)

    # Compute confidence intervals of probabilities
    compute_confidence_interval("normal execution probability", p0s, d_confidence, k)
    compute_confidence_interval("reporting probability", p1s, d_confidence, k)
    compute_confidence_interval("maintenance probability", p2s, d_confidence, k)
    compute_confidence_interval("report frequency", rfs, d_confidence, k)

    # Compute avgs
    print("Normal execution probability avg: %f" % (sum(p0s) / k))
    print("Reporting probability avg: %f" % (sum(p1s) / k))
    print("Maintenance probability avg: %f" % (sum(p2s) / k))
    print("Reporting frequency avg: %f" % (sum(rfs) / k))

def run():
    compute(1000000, 1.96, 200)

if __name__ == '__main__':
    run()
