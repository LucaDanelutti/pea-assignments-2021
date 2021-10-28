import csv

def read_dataset(file_name):
    file = open(file_name)
    file.read(1)
    csvreader = csv.DictReader(file, fieldnames = ["Arrival time", "Completion time"], 
        delimiter = ';')
    dataset = []
    for row in csvreader:
        dataset.append(row)
    file.close()
    return dataset

def compute(file_name):
    print("Computing indices for %s" % file_name)

    # Read dataset and cast values
    dataset = read_dataset(file_name)
    for job in dataset:
        job["Arrival time"] = int(job["Arrival time"])
        job["Completion time"] = int(job["Completion time"])

    start_time = dataset[0]["Arrival time"]
    print("Start time: %d" % start_time)
    end_time = dataset[-1]["Completion time"]
    print("End time: %d" % end_time)

    # Compute arrival rate and throughput
    x = len(dataset) / end_time
    print("Arrival rate and throughput: %f" % x)

    # Compute busy time
    idle_time = start_time
    for i in range(0, len(dataset)-1):
        if (dataset[i+1]["Arrival time"] > dataset[i]["Completion time"]):
            idle_time += dataset[i+1]["Arrival time"] - dataset[i]["Completion time"]
    busy_time = end_time - idle_time
    print("Busy time: %d" % busy_time)

    # Compute utilization
    utilization = busy_time / end_time
    print("Utilization: %f" % utilization)

    # Compute W
    w = 0
    for job in dataset:
        response_time = job["Completion time"] - job["Arrival time"]
        w += response_time
    print("W: %d" % w)

    # Compute average service Time - U = X * s
    avg_service_time = utilization / x
    print("Average service time: %f" % avg_service_time)

    # Compute average number of jobs - N = W / T
    avg_number_of_jobs = w / end_time
    print("Average number of jobs: %f" % avg_number_of_jobs)

    # Compute average response time - R = W / C
    avg_response_time = w / len(dataset)
    print("Average response time: %f" % avg_response_time)

    # Compute probability of m jobs (m = 0, 1, 2, 3)
    dataset_refactored = list()
    for job in dataset:
        dataset_refactored.append([job["Arrival time"], 1, 0])
        dataset_refactored.append([job["Completion time"], -1, 0])
    dataset_refactored = sorted(dataset_refactored, key = lambda x : x[0])
    for i in range(1, len(dataset_refactored)):
        dataset_refactored[i][2] = dataset_refactored[i-1][2] + dataset_refactored[i-1][1]
    intervals = list()
    intervals.append([dataset_refactored[0][0], dataset_refactored[0][2]])
    for i in range(1, len(dataset_refactored)):
        intervals.append([dataset_refactored[i][0]-dataset_refactored[i-1][0],
            dataset_refactored[i][2]])

    def compute_probability_m_jobs(m, intervals):
        cumul = 0
        for interval in intervals:
            if (interval[1] == m): cumul += interval[0]
        return cumul / end_time

    print("Probability of having no job in the station: %f" % compute_probability_m_jobs(0, intervals))
    print("Probability of having 1 job in the station: %f" % compute_probability_m_jobs(1, intervals))
    print("Probability of having 2 jobs in the station: %f" % compute_probability_m_jobs(2, intervals))
    print("Probability of having 3 jobs in the station: %f" % compute_probability_m_jobs(3, intervals))

    # Compute probability of having a response time less than tau (tau = 1, 10, 50)
    def compute_probability_response_time(tau):
        cumul = 0
        for job in dataset:
            if (job["Completion time"] - job["Arrival time"] < tau):
                cumul += 1
        return cumul / len(dataset)
    
    print("Probability of having a response time less than 1: %f" % compute_probability_response_time(1))
    print("Probability of having a response time less than 10: %f" % compute_probability_response_time(10))
    print("Probability of having a response time less than 50: %f" % compute_probability_response_time(50))

def run():
    compute("L01/DataSet1.csv")
    print("---")
    compute("L01/DataSet2.csv")

if __name__ == '__main__':
    run()