
def compute():
    l = 10 #j/s
    d1 = 0.085 #s
    d2 = 0.075 #s
    d3 = 0.050 #s

    # Compute average utilization of the three stations
    u1 = l * d1
    u2 = l * d2
    u3 = l * d3
    print("Average utilization: web server %f, DB server %f, storage server %f" % (u1, u2, u3))

    # Compute average number of jobs in the three stations
    n1 = u1 / (1 - u1)
    n2 = u2 / (1 - u2)
    n3 = u3 / (1 - u3)
    print("Average number of jobs: web server %f, DB server %f, storage server %f" % (n1, n2,n3))

    # Compute average system response time of the system
    r1 = d1 / (1 - u1)
    r2 = d2 / (1 - u2)
    r3 = d3 / (1 - u3)
    r = r1 + r2 + r3
    print("Average response time: %f" % r)

def run():
    compute()

if __name__ == '__main__':
    run()
