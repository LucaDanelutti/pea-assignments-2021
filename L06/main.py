import random
import math

def compute(n, k , m, d_confidence):
    # Generate hyper-exponential inter-arrival time trace
    hyper_exp = {}
    hyper_exp["dataset"] = []
    hyper_exp["l1"] = 0.1
    hyper_exp["l2"] = 0.05
    hyper_exp["p"] = 0.5
    def gen_hyper_exp():
        rand = random.random()
        if (rand < hyper_exp["p"]):
            return - math.log(random.random()) / hyper_exp["l1"]
        return - math.log(random.random()) / hyper_exp["l2"]
    for i in range(0, n):
        hyper_exp["dataset"].append(gen_hyper_exp())

    # Generate hypo-exponential service time trace
    hypo_exp = {}
    hypo_exp["dataset"] = []
    hypo_exp["l1"] = 0.1
    hypo_exp["l2"] = 0.5
    def gen_hypo_exp():
        return - math.log(random.random()) / hypo_exp["l1"] - math.log(random.random()) / hypo_exp["l2"]
    for i in range(0, n):
        hypo_exp["dataset"].append(gen_hypo_exp())

    # Generate arrival trace
    arrivals = []
    cumul = 0
    for i in range (0, n):
        cumul += hyper_exp["dataset"][i]
        arrivals.append(cumul)

    # Generate arrival trace
    completions = []
    completions.append(arrivals[0] + hypo_exp["dataset"][0])
    for i in range(1, n):
        completions.append(max(arrivals[i], completions[i-1]) + hypo_exp["dataset"][i])

    # Compute confidence interval
    def compute_confidence_interval(name, compute_function):
        values = []
        for i in range(0, k):
            values.append(compute_function(0 if i == 0 else completions[m*i-1], completions[m*(i+1)-1], arrivals[m*i:m*(i+1)],
                                     completions[m*i:m*(i+1)]))
        # Compute x
        cumul = 0
        for i in range(0, k):
            cumul += values[i]
        x = 1 / k * cumul
        # Compute s_square
        cumul = 0
        for i in range(0, k):
            cumul += (values[i] - x) * (values[i] - x)
        s_square = 1 / (k-1) * cumul

        print("Confidence interval of %s: [%f, %f]" % (name, x - d_confidence * math.pow(
            s_square / k, 0.5), x + d_confidence * math.pow(s_square / k, 0.5)))

    def compute_utilization(start_time, end_time, arrivals, completions):
        # Compute busy time
        idle_time = arrivals[0] - start_time
        for i in range(0, len(arrivals)-1):
            if (arrivals[i+1] > completions[i]):
                idle_time += arrivals[i+1] - completions[i]
        busy_time = (end_time - start_time) - idle_time
        utilization = busy_time / (end_time - start_time)
        return utilization

    # Compute avg. number of jobs
    def compute_num_of_jobs(start_time, end_time, arrivals, completions):
        response_time_cumul = 0
        for i in range(0, len(arrivals)):
            response_time_cumul += completions[i] - arrivals[i]
        return response_time_cumul / (end_time - start_time)

    # Compute throughput
    def compute_throughput(start_time, end_time, arrivals, completions):
        return len(completions) / (end_time - start_time)

    # Compute avg. response time
    def compute_response_time(start_time, end_time, arrivals, completions):
        response_time_cumul = 0
        for i in range(0, len(arrivals)):
            response_time_cumul += completions[i] - arrivals[i]
        return response_time_cumul / len(completions)


    print("Avg. response time: %f" % compute_response_time(0, completions[-1], arrivals, completions))
    compute_confidence_interval("avg. response time", compute_response_time)
    print("Avg. num of jobs: %f" % compute_num_of_jobs(0, completions[-1], arrivals, completions))
    compute_confidence_interval("avg. number of jobs", compute_num_of_jobs)
    print("Utilization: %f" % compute_utilization(0, completions[-1], arrivals, completions))
    compute_confidence_interval("utilization", compute_utilization)
    print("Throughput: %f" % compute_throughput(0, completions[-1], arrivals, completions))
    compute_confidence_interval("throughput", compute_throughput)

def run():
    compute(10000, 50, 200, 1.96)

if __name__ == '__main__':
    run()
