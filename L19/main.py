
def compute():
    le = 0.1 #req/s
    lc = 10 #req/s
    d1e = 2 #s
    d1c = 0.06 #s
    d2e = 5 #s
    d2c = 0.04 #s

    # Compute utilizations of the two NAS
    u1 = le * d1e + lc * d1c
    u2 = le * d2e + lc * d2c
    print("Utilizations: NAS1 %f, NAS2 %f" % (u1, u2))
    print("The system is %sstable" % ("" if all([u1 < 1, u2 < 1]) else "NOT "))

    # Compute residence times of the two NAS
    r1e = d1e / (1 - u1)
    r1c = d1c / (1 - u1)
    r2e = d2e / (1 - u2)
    r2c = d2c / (1 - u2)
    r1 = le / (le + lc) * r1e + lc / (le + lc) * r1c
    r2 = le / (le + lc) * r2e + lc / (le + lc) * r2c
    print("Residence times: NAS1 %f, NAS2 %f" % (r1, r2))

    # Compute system response time
    r = r1 + r2
    print("System response time: %f" % (r))

def run():
    compute()

if __name__ == '__main__':
    run()
