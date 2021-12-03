import numpy as np

def compute():
    N = 100 #users
    dm = 0.050 #s
    df = 0.150 #s
    da = 0.025 #s
    vm = 0.7
    vf = 0.2
    va = 1
    z = 10

    # Compute demands
    demand_m = dm * vm
    demand_f = df * vf
    demand_a = da * va
    print("Demands: %fs, %fs, %fs" % (demand_m, demand_f, demand_a))

    # Compute throughput
    qm = 0
    qf = 0
    qa = 0
    for n in range(1, N+1):
        rm = demand_m * (1 + qm)
        rf = demand_f * (1 + qf)
        ra = demand_a * (1 + qa)
        x = n / (z + rm + rf + ra)
        qm = x * rm
        qf = x * rf
        qa = x * ra
    print("System throughput: %f" % x)

    # Compute system response time
    r = rm + rf + ra
    print("System response time: %f" % r)


def run():
    compute()

if __name__ == '__main__':
    run()
