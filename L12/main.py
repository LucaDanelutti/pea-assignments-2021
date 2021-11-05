import math

def compute():
    # Parameters
    l = 10 # job/s
    d = 0.085 # s
    mi = 1 / d

    # Compute p
    p = d * l 
    print("p: %f" % p)

    # Compute utilization
    u = p
    print("Utilization: %f" % u)

    # Compute probability of having 1 job in the system
    p_one_job = 1 - p * p - (1-u)
    print("Probability of having one job in the system: %f" % p_one_job)

    # Compute probability of having more than 5 jobs in the system
    p_more_five_job = math.pow(p, 6) 
    print("Probability of having more than 5 jobs in the system: %f" % p_more_five_job)

    # Compute average queue lenght
    avg_queue_time = p * d / (1-p)
    avg_queue_length = avg_queue_time * l
    print("Average queue length: %f" % avg_queue_length)

    # Compute average response time
    avg_r = 1 / (mi - l)
    print("Average response time: %f" % avg_r)

    # Compute probability that the avg r is greater than 0.5s
    p_r_greater_05 = math.pow(math.e, -(0.5/avg_r))
    print("Probability that the avg r is greater than 0.5s: %f" % p_r_greater_05)

    # Compute the 90 percentile of r
    r_percentile_90 = - math.log(1 - 0.9) * avg_r
    print("90th percentile of response time: %f" % r_percentile_90)

def run():
    compute()


if __name__ == '__main__':
    run()
