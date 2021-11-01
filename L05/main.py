import random
import math
import statistics
import numpy as np
import matplotlib.pyplot as plt

def generate(n):
    # Generate uniform dataset
    uniform = {}
    uniform["Dataset"] = []
    uniform["a"] = 10
    uniform["b"] = 20
    for i in range(0, n):
        uniform["Dataset"].append(uniform["a"] + (uniform["b"]-uniform["a"]) * random.random())

    # Generate discrete distribution
    discrete = {}
    discrete["Dataset"] = []
    discrete["p1"] = 0.2
    discrete["value1"] = 5
    discrete["p2"] = 0.6
    discrete["value2"] = 15
    discrete["p3"] = 0.2
    discrete["value3"] = 20
    def gen_discrete():
        rand = random.random()
        if (rand < discrete["p1"]): return discrete["value1"]
        if (rand < discrete["p1"]+discrete["p2"]): return discrete["value2"]
        return discrete["value3"]
    for i in range(0, n):
        discrete["Dataset"].append(gen_discrete())
    
    # Generate exponential distribution
    exponential = {}
    exponential["Dataset"] = []
    exponential["l"] = 1 / 15
    def gen_exp():
        return - math.log(random.random()) / exponential["l"]
    for i in range(0, n):
        exponential["Dataset"].append(gen_exp())

    # Generate hyper-exponential distribution
    hyper_exp = {}
    hyper_exp["Dataset"] = []
    hyper_exp["l1"] = 0.1
    hyper_exp["l2"] = 0.05
    hyper_exp["p"] = 0.5
    def gen_hyper_exp():
        rand = random.random()
        if (rand > hyper_exp["p"]):
            return - math.log(random.random()) / hyper_exp["l1"]
        return - math.log(random.random()) / hyper_exp["l2"]
    for i in range(0, n):
        hyper_exp["Dataset"].append(gen_hyper_exp())

    # Generate hypo-exponential distribution
    hypo_exp = {}
    hypo_exp["Dataset"] = []
    hypo_exp["l1"] = 0.1
    hypo_exp["l2"] = 0.2
    def gen_hypo_exp():
        return - math.log(random.random()) / hypo_exp["l1"] - math.log(random.random()) / hypo_exp["l2"]
    for i in range(0, n):
        hypo_exp["Dataset"].append(gen_hypo_exp())

    # Generate hyper-erlang distribution
    hyper_erlang = {}
    hyper_erlang["Dataset"] = []
    hyper_erlang["l1"] = 0.02
    hyper_erlang["k1"] = 1
    hyper_erlang["p1"] = 0.1
    hyper_erlang["l2"] = 0.2
    hyper_erlang["k2"] = 2
    hyper_erlang["p2"] = 0.4
    hyper_erlang["l3"] = 0.25
    hyper_erlang["k3"] = 3
    hyper_erlang["p3"] = 0.5
    def gen_hyper_erlang():
        rand = random.random()
        if (rand < hyper_erlang["p1"]):
            res = 0
            for i in range(0, hyper_erlang["k1"]):
                res -= (math.log(random.random())/hyper_erlang["l1"])
            return res
        if (rand < hyper_erlang["p1"]+hyper_erlang["p2"]):
            res = 0
            for i in range(0, hyper_erlang["k2"]):
                res -= (math.log(random.random())/hyper_erlang["l2"])
            return res
        res = 0
        for i in range(0, hyper_erlang["k3"]):
            res -= (math.log(random.random())/hyper_erlang["l3"])
        return res
    for i in range(0, n):
        hyper_erlang["Dataset"].append(gen_hyper_erlang())

    # Compute averages
    def moment(n, dataset):
        cumul = 0
        for time in dataset:
            cumul += pow(time, n)
        return cumul / len(dataset)
    uniform_avg = moment(1, uniform["Dataset"])
    discrete_avg = moment(1, discrete["Dataset"])
    exponential_avg = moment(1, exponential["Dataset"])
    hyper_exp_avg = moment(1, hyper_exp["Dataset"])
    hypo_exp_avg = moment(1, hypo_exp["Dataset"])
    hyper_erlang_avg = moment(1, hyper_erlang["Dataset"])
    print("Gen. uniform avg: %f" % uniform_avg)
    print("Uniform avg: %f" % ((uniform["b"]-uniform["a"])/2 + uniform["a"]))
    print("Gen. discrete avg: %f" % discrete_avg)
    print("Discrete avg: %f" % (discrete["p1"]*discrete["value1"]+discrete["p2"]*discrete["value2"]+discrete["p3"]*discrete["value3"]))
    print("Gen. exponential avg: %f" % exponential_avg)
    print("Exponential avg: %f" % (1/exponential["l"]))
    print("Gen. hyper-exponential avg: %f" % hyper_exp_avg)
    print("Hyper-exponential avg: %f" % (hyper_exp["p"] / hyper_exp["l1"] + hyper_exp["p"] / hyper_exp["l2"]))
    print("Gen. hypo-exponential avg: %f" % hypo_exp_avg)
    print("Hypo-exponential avg: %f" % (1 / hypo_exp["l1"] + 1 / hypo_exp["l2"]))
    print("Gen. hyper-erlang avg: %f" % hyper_erlang_avg)
    print("Hyper-erlang avg: %f" % (hyper_erlang["k1"]/hyper_erlang["l1"]*hyper_erlang["p1"] \
        + hyper_erlang["k2"]/hyper_erlang["l2"]*hyper_erlang["p2"] + hyper_erlang["k3"]/hyper_erlang["l3"]*hyper_erlang["p3"]))

    # Compute std dev
    uniform_std_dev = statistics.stdev(uniform["Dataset"])
    discrete_std_dev = statistics.stdev(discrete["Dataset"])
    exponential_std_dev = statistics.stdev(exponential["Dataset"])
    hyper_exp_std_dev = statistics.stdev(hyper_exp["Dataset"])
    hypo_exp_std_dev = statistics.stdev(hypo_exp["Dataset"])
    hyper_erlang_std_dev = statistics.stdev(hyper_erlang["Dataset"])
    print("Gen. uniform std dev: %f" % uniform_std_dev)
    print("Gen. discrete std dev: %f" % discrete_std_dev)
    print("Gen. exponential std dev: %f" % exponential_std_dev)
    print("Gen. hyper-exponential std dev: %f" % hyper_exp_std_dev)
    print("Gen. hypo-exponential std dev: %f" % hypo_exp_std_dev)
    print("Gen. hyper-erlang std dev: %f" % hyper_erlang_std_dev)

    # Compute coefficient of variation
    uniform_cv = uniform_std_dev / uniform_avg
    discrete_cv = discrete_std_dev / discrete_avg
    exponential_cv = exponential_std_dev / exponential_avg
    hyper_exp_cv = hyper_exp_std_dev / hyper_exp_avg
    hypo_exp_cv = hypo_exp_std_dev / hypo_exp_avg
    hyper_erlang_cv = hyper_erlang_std_dev / hyper_erlang_avg
    print("Gen. uniform cv: %f" % uniform_cv)
    print("Gen. discrete cv: %f" % discrete_cv)
    print("Gen. exponential cv: %f" % exponential_cv)
    print("Gen. hyper-exponential cv: %f" % hyper_exp_cv)
    print("Gen. hypo-exponential cv: %f" % hypo_exp_cv)
    print("Gen. hyper-erlang cv: %f" % hyper_erlang_cv)

    # Plot CDFs
    x = np.linspace(0, 50, 500)
    def plot(dataset, label):
        ordered_dataset = sorted(dataset)
        cdf = []
        i = 1/len(ordered_dataset)
        for time in ordered_dataset:
            cdf.append((time, i))
            i += 1/len(ordered_dataset)
        plt.plot([item[0] for item in cdf], [item[1]
                                            for item in cdf], label=label)
    plot(uniform["Dataset"], "Uniform")
    plot(discrete["Dataset"], "Discrete")
    plot(exponential["Dataset"], "Exp")
    plot(hyper_exp["Dataset"], "Hyper exp")
    plot(hypo_exp["Dataset"], "Hypo exp")
    plot(hyper_erlang["Dataset"], "Hyper erlang")
    plt.xlim(left=-15, right=50)
    plt.ylim(bottom=0, top=1)
    plt.legend()
    plt.show()

def run():
    generate(500)

if __name__ == '__main__':
    run()
