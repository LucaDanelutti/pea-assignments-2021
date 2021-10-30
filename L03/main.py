import math
import matplotlib.pyplot as plt

def read_dataset(file_name):
    file = open(file_name)
    dataset = []
    for line in file:
        dataset.append(line.splitlines()[0])
    file.close()
    return dataset

def compute(file_name):
    print("Computing indices for %s" % file_name)

    # Read dataset and cast values
    dataset_str = read_dataset(file_name)
    dataset = []
    for time in dataset_str:
        dataset.append(float(time))

    # Compute moments
    def moment(n):
        cumul = 0
        for time in dataset:
            cumul += pow(time, n)
        return cumul / len(dataset)
    first_moment = moment(1)
    second_moment = moment(2)
    third_moment = moment(3)
    fourth_moment = moment(4)
    print("First moment: %f" % first_moment)
    print("Second moment: %f" % second_moment)
    print("Third moment: %f" % third_moment)
    print("Fourth moment: %f" % fourth_moment)

    # Compute second, third and fourth centered moments
    sigma_square = second_moment - pow(first_moment, 2)
    print("Second centered moment: %f" % sigma_square)

    def centered_moment(n):
        cumul = 0
        for time in dataset:
            cumul += pow(time - first_moment, n)
        return cumul / len(dataset)
    second_centered_moment = centered_moment(2)
    third_centered_moment = centered_moment(3)
    fourth_centered_moment = centered_moment(4)
    print("Second centered moment (alternative computation): %f" % second_centered_moment)
    print("Third centered moment: %f" % third_centered_moment)
    print("Fourth centered moment: %f" % fourth_centered_moment)

    # Compute third and fourth standardized moments
    def standardized_moment(n):
        if (second_centered_moment == 0): return float("nan")
        cumul = 0
        for time in dataset:
            cumul += pow((time - first_moment)/pow(second_centered_moment, 0.5), n)
        return cumul / len(dataset)
    third_standardized_moment = standardized_moment(3)
    fourth_standardized_moment = standardized_moment(4)
    print("Third standardized moment: %f" % third_standardized_moment)
    print("Fourth standardized moment: %f" % fourth_standardized_moment)

    # Compute standard deviation, coefficient of variation and Kurtosis
    standard_deviation = pow(second_centered_moment, 0.5)
    coefficient_variation = standard_deviation/first_moment
    kurtosis = fourth_standardized_moment - 3
    print("Standard deviation: %f" % standard_deviation)
    print("Coefficient of variation: %f" % coefficient_variation)
    print("Kurtosis: %f" % kurtosis)

    # Compute percentiles
    ordered_dataset = sorted(dataset)
    def percentile(k):
        index = len(dataset) * k / 100
        return ordered_dataset[math.ceil(index)-1]
    print("10%% percentile: %f" % percentile(10))
    print("25%% percentile: %f" % percentile(25))
    print("50%% percentile: %f" % percentile(50))
    print("75%% percentile: %f" % percentile(75))
    print("90%% percentile: %f" % percentile(90))

    # Compute cross-covariance
    def cross_covariance(lag):
        cumul = 0
        for i in range(0, len(dataset) - lag):
            cumul += (dataset[i] -
                      first_moment) * (dataset[i+lag] - first_moment)
        return cumul / (len(dataset)-lag)
    one_cross_covariance = cross_covariance(1)
    two_cross_covariance = cross_covariance(2)
    three_cross_covariance = cross_covariance(3)
    print("Cross-covariance for lag = 1: %f" % one_cross_covariance)
    print("Cross-covariance for lag = 2: %f" % two_cross_covariance)
    print("Cross-covariance for lag = 3: %f" % three_cross_covariance)

    # Compute CDF
    cdf = []
    i = 1/len(ordered_dataset)
    for time in ordered_dataset:
        cdf.append((time, i))
        i += 1/len(ordered_dataset)
    plt.plot([item[0] for item in cdf], [item[1] for item in cdf])
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.show()
    input("Press enter to continue")

def run():
    compute("L03/Data1.txt")
    print("---")
    compute("L03/Data2.txt")
    print("---")
    compute("L03/Data3.txt")
    print("---")
    compute("L03/Data4.txt")

if __name__ == '__main__':
    run()
