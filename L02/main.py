import re
from datetime import datetime
import statistics
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as stattools

def read_dataset(file_name):
    file = open(file_name)
    regex = '([\d\.]+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'
    dataset = []
    for row in file:
        groups = re.match(regex, row).groups()
        datetime_object = datetime.strptime(groups[1], '%d/%b/%Y:%H:%M:%S %z')
        dataset.append(datetime_object)
    file.close()
    return dataset

def compute(file_name):
    print("Computing indices for %s" % file_name)
    dataset = read_dataset(file_name)
    
    # Compute inter arrival times
    inter_arrival_times = list()
    for i in range(0, len(dataset)-1):
        inter_arrival_times.append((dataset[i+1]-dataset[i]).total_seconds())
    
    # Compute arrival rate
    t = (dataset[-1]-dataset[0]).total_seconds()
    avg_arrival_rate = len(dataset) / t
    print("Average arrival rate: %f jobs/second" % avg_arrival_rate)

    # Compute avg. inter arrival time
    cumul = 0
    for time in inter_arrival_times:
        cumul += time
    avg_inter_arrival_time = cumul / len(inter_arrival_times)
    print("Average inter arrival time: %f seconds" % avg_inter_arrival_time)

    # Compute coefficient of variation | cv = std. dev. / mean
    standard_deviation = statistics.stdev(inter_arrival_times)
    cv = standard_deviation / avg_inter_arrival_time
    print("Coefficient of variation: %f" % cv)

    # Compute covariance (sigma(1))
    covariance = stattools.acovf(inter_arrival_times, fft=False, nlag=1)[1]
    print("Correlation: %f" % covariance)

    # Alternative computation of covariance (sigma(1))
    cumul = 0
    for i in range(0, len(inter_arrival_times)-1):
        cumul += (inter_arrival_times[i] -
                  avg_inter_arrival_time) * (inter_arrival_times[i+1] - avg_inter_arrival_time)
    covariance = cumul / (len(inter_arrival_times)-1)
    print("Correlation (approximated): %f" % covariance)

    # Plotting x and y to show correlation
    plt.scatter(inter_arrival_times[0:-2], inter_arrival_times[1:-1], s=2)
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.show()
    input("Press enter to continue")

def run():
    compute("L02/Log1.txt")
    compute("L02/Log2.txt")
    compute("L02/Log3.txt")
    compute("L02/Log4.txt")

if __name__ == '__main__':
    run()
