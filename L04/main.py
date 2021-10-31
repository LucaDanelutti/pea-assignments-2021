import csv
import numpy as np
import matplotlib.pyplot as plt
import matlab.engine

def read_dataset(file_name, webserver_id):
    file = open(file_name)
    csvreader = csv.DictReader(file, fieldnames=["Webserver 1", "Webserver 2", "Webserver 3", "Webserver 4"],
                               delimiter=',')
    dataset_str = []
    for row in csvreader:
        dataset_str.append(row)
    file.close()

    dataset = []
    for entry in dataset_str:
        dataset.append({"Webserver 1": float(entry["Webserver 1"]),
                        "Webserver 2": float(entry["Webserver 2"]),
                        "Webserver 3": float(entry["Webserver 3"]),
                        "Webserver 4": float(entry["Webserver 4"])})
    return [entry["Webserver " + str(webserver_id)] for entry in dataset]

def compute_moments(file_name, webserver_id):
    print("Computing indices for %s webserver %s" % (file_name, str(webserver_id)))

    # Read dataset and cast values 
    dataset = read_dataset(file_name, webserver_id)
    
    # Fit data against uniform, exponential, hyperexponential, hypoexponential using moments
    print("Using moments:")
    
    # Uniform: a and b
    def moment(n):
        cumul = 0
        for time in dataset:
            cumul += pow(time, n)
        return cumul / len(dataset)
    first_moment = moment(1)
    second_moment = moment(2)
    a = first_moment - 0.5 * pow((12*(second_moment-pow(first_moment, 2))), 0.5)
    b = first_moment + 0.5 * pow((12*(second_moment-pow(first_moment, 2))), 0.5)
    print("Uniform | a: %f" % a)
    print("Uniform | b: %f" % b)

    # Exponential: lambda
    exponential_lambda = 1 / first_moment
    print("Exponential | lambda: %f" % exponential_lambda)

    # Hyperexponential: p, lambda1, lambda2
    p = 0.4
    hyper_lambda1 = 0.8 / first_moment
    hyper_lambda2 = 1.2 / first_moment
    print("Hyperexponential | p: %f" % p)
    print("Hyperexponential | lambda1: %f" % hyper_lambda1)
    print("Hyperexponential | lambda2: %f" % hyper_lambda2)

    # Hypoexponential: lambda1, lambda2
    hypo_lambda1 = 1 / (0.3*first_moment)
    hypo_lambda2 = 1 / (0.7*first_moment)
    print("Hypoexponential | lambda1: %f" % hypo_lambda1)
    print("Hypoexponential | lambda2: %f" % hypo_lambda2)

    # Compute CDF of fitted distributions
    x = np.linspace(0, 50, 5000)
    uniform = (x - a) / (b - a)
    exponential = 1 - np.power(np.e, - (exponential_lambda * x))
    hyperexponential = 1 - \
        p * np.power(np.e, - (hyper_lambda1 * x)) - \
        (1-p) * np.power(np.e, - (hyper_lambda2 * x))
    hypoexponential = 1 - \
        (hypo_lambda2 * np.power(np.e, - (hypo_lambda1 * x))) / (hypo_lambda2 - hypo_lambda1) + \
        (hypo_lambda1 * np.power(np.e, - (hypo_lambda2 * x))) / (hypo_lambda2 - hypo_lambda1)

    # Compute CDF of dataset
    ordered_dataset = sorted(dataset)
    cdf = []
    i = 1/len(ordered_dataset)
    for time in ordered_dataset:
        cdf.append((time, i))
        i += 1/len(ordered_dataset)

    # Plot CDFs
    plt.plot([item[0] for item in cdf], [item[1] for item in cdf], label="Dataset")
    plt.plot(x, uniform, label="Uniform")
    plt.plot(x, exponential, label="Exp")
    plt.plot(x, hyperexponential, label="Hyperexp")
    plt.plot(x, hypoexponential, label="Hypoexp")
    plt.xlim(left=-15, right=50)
    plt.ylim(bottom=0, top=1)
    plt.legend()
    plt.show()
    # input("Press enter to continue")

def compute_maximum_likelihood(file_name, webserver_id):
    print("Computing indices for %s webserver %s" % (file_name, str(webserver_id)))

    # Read dataset and cast values
    dataset = read_dataset(file_name, webserver_id)
    
    # Fit data against uniform, exponential, hyperexponential, hypoexponential using maximum likelihood
    print("Using maximum likelihood:")

    # Exponential: lambda
    cumul = 0
    for time in dataset:
        cumul += time
    exponential_lambda = len(dataset) / cumul
    print("Exponential: %f" % exponential_lambda)

    # Setting up matlab engine
    eng = matlab.engine.start_matlab()
    matlab_dataset = matlab.double(dataset)
    eng.workspace['dataset'] = matlab_dataset

    # Hyperexponential: p, lambda1, lambda2
    estimations = eng.eval(
        "mle(dataset, 'pdf', @(x, l1, l2, p) \
             p * l1 * exp(-l1 * x) + (1-p) * l2 * exp(-l2 * x), 'Start', [0.5, 0.5, 0.5], 'LowerBound', [0, 0, 0], 'UpperBound', [Inf, Inf, 1])")
    hyper_lambda1 = estimations[0][0]
    hyper_lambda2 = estimations[0][1]
    p = estimations[0][2]
    print("Hyperexponential | p: %f" % p)
    print("Hyperexponential | lambda1: %f" % hyper_lambda1)
    print("Hyperexponential | lambda2: %f" % hyper_lambda2)

    # Hypoexponential: lambda1, lambda2
    estimations = eng.eval(
        "mle(dataset, 'pdf', @(x, l1, l2) \
             (l1 * l2) / (l1 - l2) * (exp(-l2 * x) - exp(-l1 * x)), 'Start', [0.45, 0.55], 'LowerBound', [0, 0], 'UpperBound', [Inf, Inf])")
    hypo_lambda1 = estimations[0][0]
    hypo_lambda2 = estimations[0][1]
    print("Hypoexponential | lambda1: %f" % hypo_lambda1)
    print("Hypoexponential | lambda2: %f" % hypo_lambda2)

    # Quitting matlab engine
    eng.quit()

    # Compute CDF of fitted distributions
    x = np.linspace(0, 50, 5000)
    exponential = 1 - np.power(np.e, - (exponential_lambda * x))
    hyperexponential = 1 - \
        p * np.power(np.e, - (hyper_lambda1 * x)) - \
        (1-p) * np.power(np.e, - (hyper_lambda2 * x))
    hypoexponential = 1 - \
        (hypo_lambda2 * np.power(np.e, - (hypo_lambda1 * x))) / (hypo_lambda2 - hypo_lambda1) + \
        (hypo_lambda1 * np.power(np.e, - (hypo_lambda2 * x))) / \
        (hypo_lambda2 - hypo_lambda1)

    # Compute CDF of dataset
    ordered_dataset = sorted(dataset)
    cdf = []
    i = 1/len(ordered_dataset)
    for time in ordered_dataset:
        cdf.append((time, i))
        i += 1/len(ordered_dataset)

    # Plot CDFs
    plt.plot([item[0] for item in cdf], [item[1]
                                         for item in cdf], label="Dataset")
    plt.plot(x, exponential, label="Exp")
    plt.plot(x, hyperexponential, label="Hyperexp")
    plt.plot(x, hypoexponential, label="Hypoexp")
    plt.xlim(left=-15, right=50)
    plt.ylim(bottom=0, top=1)
    plt.legend()
    plt.show()
    input("Press enter to continue")

def run():
    compute_maximum_likelihood("L04/Traces.csv", 3)
    print("---")
    compute_moments("L04/Traces.csv", 3)

if __name__ == '__main__':
    run()
