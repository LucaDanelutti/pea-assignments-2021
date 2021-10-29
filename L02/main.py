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

def run():
    dataset = read_dataset("L02/Log1.txt")
    
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

    # Compute covariance (sigma=1)
    covariance = stattools.acovf(inter_arrival_times, fft=False, nlag=1)[1]
    print("Correlation: %f" % covariance)

    # Plotting x and y to show correlation
    plt.scatter(x, y, s=2)
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.show()
    input()

if __name__ == '__main__':
    run()