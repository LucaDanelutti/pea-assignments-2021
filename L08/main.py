import random
import math

def compute(total_t):
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

def run():
    compute(1000000)

if __name__ == '__main__':
    run()
