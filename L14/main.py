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

    # Compute throughput and drop rate
    x = l
    drop_rate = 0
    print("Throughput: %f" % x)
    print("Drop rate: %f" % drop_rate)

    # Compute average response time and queue time
    r = n / l
    queue_time = r - d
    print("Average response time: %f" % r)
    print("Average queue time: %f" % queue_time)
    print()

def compute_with_capacity(l, d, c, k):
    print("--- M/M/%d/%d with l = %f, D = %f ---" % (c, k, l, d))
    mi = 1 / d
    p = l / mi / c 

    # Compute probability of having n jobs in the system
    def compute_probability_n_jobs(n):
        sum = 0
        for i in range(0, c):
            sum += pow(c*p, i) / math.factorial(i)
        pi_0 = math.pow(pow(c*p, c) / math.factorial(c) / (1-p) * (1 - pow(p, k - c + 1)) + sum, -1)
        if n == 0:
            pi = pi_0
        elif n < c:
            pi = pi_0 / math.factorial(n) * math.pow(c * p, n)
        elif n <= k:
            pi = pi_0 * math.pow(c, c) * math.pow(p, n) / math.factorial(c)
        else:
            pi = 0
        return pi

    # Compute average utilization
    u = 0
    for i in range(1, c+1):
        u += i * compute_probability_n_jobs(i)
    for i in range(c+1, k+1):
        u += c * compute_probability_n_jobs(i)
    u = u / c
    print("Average utilization: %f" % u)

    # Compute probability of having 4 jobs in the system
    print("Probability of having 4 jobs in the system: %f" % compute_probability_n_jobs(4))

    # Compute average number of jobs in the system
    n = 0
    for i in range (0, k+1):
        n += i * compute_probability_n_jobs(i)
    print("Average number of jobs in the system: %f" % n)

    # Compute throughput and drop rate
    drop_rate = compute_probability_n_jobs(k) * l
    x = l * (1 - compute_probability_n_jobs(k))
    print("Throughput: %f" % x)
    print("Drop rate: %f" % drop_rate)

    # Compute average response time and queue time
    r = n / (l * (1 - compute_probability_n_jobs(k)))
    queue_time = r - d
    print("Average response time: %f" % r)
    print("Average queue time: %f" % queue_time)
    print()

def run():
    # ES1 M/M/1/6 l=0.9j/s D=1s
    print("ES1")
    compute_with_capacity(0.9, 1.0, 1, 6)
    # Compare with a MM1
    compute(0.9, 1.0, 1)

    # ES2 MM2 l=01.8j/s D=1s
    print("ES2")
    compute_with_capacity(1.8, 1.0, 2, 6)
    # Compare with a MM2
    compute(1.8, 1.0, 2)

if __name__ == '__main__':
    run()
