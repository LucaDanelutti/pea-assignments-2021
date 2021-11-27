import numpy as np

def compute():
    l1 = 0.5 #j/s
    s = np.zeros((3))
    s[0] = 1
    s[1] = 2
    s[2] = 2.5

    p = np.zeros((3, 3))
    p[0][0] = 0.7
    p[0][1] = 0.3
    p[1][0] = 0.5
    p[1][2] = 0.3
    p[2][1] = 1

    l = np.zeros((3))
    l[0] = l1 / l1

    # Compute visits of the three stations
    v = np.matmul(l, np.linalg.matrix_power(np.subtract(np.identity(3), p), -1))
    print("Visits: server1 %f, server2 %f, server3 %f" % (v[0], v[1], v[2]))

    # Compute demands of the three stations
    d = np.multiply(v, s)
    print("Demands: server1 %f, server2 %f, server3 %f" % (d[0], d[1], d[2]))

    # Compute stability
    l_limit = 1 / max(d)
    print("Lambda limit: %f -> system is %s stable" % (l_limit, "" if l1 < l_limit else "NOT"))

    # Compute stability (alternative)
    u = np.zeros((3))
    u[0] = d[0] * l1
    u[1] = d[1] * l1
    u[2] = d[2] * l1
    print("Utilizations: server1 %f, server2 %f, server3 %f -> system is %s stable" % (u[0], u[1], u[2], "" if all(u) < 1 else "NOT"))

def run():
    compute()

if __name__ == '__main__':
    run()
