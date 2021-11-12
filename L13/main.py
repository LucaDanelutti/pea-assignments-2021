import math

def compute(l, d, c):
    print("--- MM%d with l = %f, D = %f ---" % (c, l, d))
    mi = 1 / d

    # Compute average utilization
    p = l / mi / c 
    u = p
    print("Average utilization: %f" % u)

    # Compute probability of having 4 jobs in the system
    summation = 0
    for i in range(0, c):
        summation += pow(c*p, i) / math.factorial(i)
    pi_0 = math.pow(pow(c*p, c) / math.factorial(c) / (1-p) + summation, -1)
    if c <= 4:
        pi_4 = pi_0 * math.pow(c, c) * math.pow(p, 4) / math.factorial(c)
    else:
        pi_4 = pi_0 / math.factorial(4) * math.pow(c * p, 4)
    print("Probability of having 4 jobs in the system: %f" % pi_4)

    # Compute average number of jobs in the system
    summation = 0
    for i in range (0, c):
        summation += math.pow(c * p, i) / math.factorial(i)
    n = c * p + (p / (1 - p)) / (1 + (1 - p) * (math.factorial(c) / math.pow(c * p, c)) * summation)
    print("Average number of jobs in the system: %f" % n)

    # Compute average response time and queue time
    r = n / l
    queue_time = r - d
    print("Average response time: %f" % r)
    print("Average queue time: %f" % queue_time)
    print()

def compute_mminf(l, d):
    print("--- MM%s with l = %f, D = %f ---" % ("inf", l, d))

    # Compute p
    p = l * d

    # Compute probability of having 4 jobs in the system
    pi_0 = math.pow(math.e, -p)
    pi_4 = pi_0 * math.pow(p, 4) / math.factorial(4)
    print("Probability of having 4 jobs in the system: %f" % pi_4)

    # Compute average number of jobs in the system
    n = p
    print("Average number of jobs in the system: %f" % n)

    # Compute average response time and queue time
    r = d
    queue_time = r - d
    print("Average response time: %f" % r)
    print("Average queue time: %f" % queue_time)
    print()

def run():
    # ES1 MM2 l=0.95j/s D=1.8s
    print("ES1")
    compute(0.95, 1.8, 2)
    # Compare with a MM1 D=0.9s
    compute(0.95, 0.9, 1)

    # ES2 MM3 l=0.95j/s D=2.7s
    print("ES2")
    compute(0.95, 2.7, 3)
    # Compare with MM1 D=0.9s and MM2 D=1.8s (already printed)

    # ES3 MMinf l=0.95j/s D=2.7s
    print("ES3")
    compute_mminf(0.95, 2.7)
    # Compare with MM1 D=0.9s, MM2 D=1.8s and MM3 D=2.7s (already printed)

if __name__ == '__main__':
    run()
