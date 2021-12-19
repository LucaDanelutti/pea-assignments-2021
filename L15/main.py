
def compute_mg1(l, p1, u1, u2):
    print("--- MG1 with l = %f, service time hyperexp with p1 = %f, u1 = %f, u2 = %f ---" % (l, p1, u1, u2))
    # Compute mean service time (d) and service time rate (mi)
    d = p1 / u1 + (1 - p1) / u2
    mi = 1 / d

    # Compute variance and coefficient of variation
    m2 = 2 * (p1 / pow(u1, 2) + (1-p1) / pow(u2, 2))
    var = m2 - pow(d, 2)
    cv2 = var / pow(d, 2)

    # Compute utilization
    p = l / mi
    u = p
    print("Utilization: %f" % u)

    # Compute average number of jobs in the system
    n = p + pow(p, 2) * (1 + cv2) / 2 / (1-p)
    print("Average number of jobs in the system: %f" % n)

    # Compute average response
    r = d + p*d / (1-p) * (1+cv2) / 2
    # Alternative r = d + l*m2 / 2 / (1-p)
    print("Average response time: %f" % r)
    print()

def compute_gg2(a, b, p1, u1, u2):
    print("--- GG2 with inter arrival rate uniform with a = %f, b = %f, service time hyperexp with \
         p1 = %f, u1 = %f, u2 = %f ---" % (a, b, p1, u1, u2))
    # Compute inter arrival time rate (l), mean service time (d) and service time rate (mi)
    l = 1 / ((a + b) / 2)
    d = p1 / u1 + (1 - p1) / u2
    mi = 1 / d

    # Compute variance and coefficient of variation
    # Uniform
    var = pow((b - a), 2)/12
    ca2 = var / pow(1 / l, 2)
    # Hyperexp
    m2 = 2 * (p1 / pow(u1, 2) + (1-p1) / pow(u2, 2))
    var = m2 - pow(d, 2)
    cv2 = var / pow(d, 2)

    # Compute utilization
    p = l / mi / 2
    u = p * 2
    print("Utilization: %f" % u)

    # Compute approximated average response
    queue_time_mm2 = 2*p / (1-pow(p, 2)) / l - d
    # Alternative queue_time_mm2 = pow(p, 2) * d / (1-pow(p, 2))
    r = d + (ca2 + cv2) / 2 * queue_time_mm2
    print("Approximated average response time: %f" % r)

    # Compute approximated average number of jobs
    n = l * r
    print("Approximated average number of jobs: %f" % n)
    print()

def run():
    # ES1 MG1 l=3j/s, hyperexp u1=1j/s u2=10j/s p1=0.2
    print("ES1")
    compute_mg1(3, 0.2, 1, 10)

    # ES2 GG2 arrival uniform 0.1-0.2, hyperexp u1=1j/s u2=10j/s p1=0.2
    print("ES2")
    compute_gg2(0.1, 0.2, 0.2, 1, 10)

if __name__ == '__main__':
    run()
