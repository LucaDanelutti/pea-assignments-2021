from scipy.integrate import odeint
import numpy as np
import scipy

def compute():
    # CPU parameters
    l_a_exec_full = 1 / 8
    l_a_exec_half = l_a_exec_full / 2
    l_a_wait = 1 / 10
    l_b_exec_full = 1 / 12
    l_b_exec_half = l_b_exec_full / 2
    l_b_wait = 1 / 5

    # Generate infinitesimal generator matrix
    infinitesimal_generator = np.zeros((4, 4))
    infinitesimal_generator[0][1] = l_b_exec_half
    infinitesimal_generator[0][2] = l_a_exec_half
    infinitesimal_generator[1][3] = l_a_exec_full
    infinitesimal_generator[2][3] = l_b_exec_full
    infinitesimal_generator[1][0] = l_b_wait
    infinitesimal_generator[2][0] = l_a_wait
    infinitesimal_generator[3][1] = l_a_wait
    infinitesimal_generator[3][2] = l_b_wait

    infinitesimal_generator[0][0] = - sum(infinitesimal_generator[0])
    infinitesimal_generator[1][1] = - sum(infinitesimal_generator[1])
    infinitesimal_generator[2][2] = - sum(infinitesimal_generator[2])
    infinitesimal_generator[3][3] = - sum(infinitesimal_generator[3])

    # Define pi(0) initial condition
    s0 = np.zeros((4))
    s0[0] = 1

    # Define Q'
    infinitesiaml_generator_prime = np.copy(infinitesimal_generator)
    infinitesiaml_generator_prime[0][0] = 1
    infinitesiaml_generator_prime[1][0] = 1
    infinitesiaml_generator_prime[2][0] = 1
    infinitesiaml_generator_prime[3][0] = 1

    # Compute stationary solution
    y_stationary = np.matmul(s0, np.linalg.inv(infinitesiaml_generator_prime))

    # Define differential equation
    def equation(y, x):
        dydt = np.dot(y, infinitesimal_generator)
        return dydt

    # Print probabilities
    print("Stationary probability of Exec-Exec: %f" % y_stationary[0])
    print("Stationary probability of Exec-Wait: %f" % y_stationary[1])
    print("Stationary probability of Wait-Exec: %f" % y_stationary[2])
    print("Stationary probability of Wait-Wait: %f" % y_stationary[3])

    # Compute utilization and avg. number of tasks
    print("Utilization: %f" %
          (y_stationary[0] + y_stationary[1] + y_stationary[2]))
    print("Average number of tasks: %f" %
          (2*y_stationary[0] + 1*y_stationary[1] + 1*y_stationary[2]))

    # Compute throughput
    print("Throughput: %f" % (y_stationary[0]*l_b_exec_half*1 + y_stationary[1]*l_a_exec_full*1 + 
        y_stationary[2]*l_b_exec_full*1 + y_stationary[0]*l_a_exec_half*1))

    # Compute transient y using differential equation
    def compute_avg_number_of_jobs(t):
        # Define x
        x = np.linspace(0, t, t)
        # Solve differential equation
        y = odeint(equation, s0, x)
        print("Avg. number of jobs at t=%d: %f" %
              (t, (2*y[t-1][0] + 1*y[t-1][1] + 1*y[t-1][2])))
    
    # Compute avg. number of jobs at 10, 20, 50, 100
    compute_avg_number_of_jobs(10)
    compute_avg_number_of_jobs(20)
    compute_avg_number_of_jobs(50)
    compute_avg_number_of_jobs(100)

    # Compute transient y using matrix exponential
    def compute_avg_number_of_jobs_alternative(t):
        # Define x
        x = np.linspace(0, t, t)
        
        y = np.matmul(s0, scipy.linalg.expm(infinitesimal_generator*t))

        print("Avg. number of jobs at t=%d: %f" %
              (t, (2*y[0] + 1*y[1] + 1*y[2])))

    # Compute avg. number of jobs at 10, 20, 50, 100
    compute_avg_number_of_jobs_alternative(10)
    compute_avg_number_of_jobs_alternative(20)
    compute_avg_number_of_jobs_alternative(50)
    compute_avg_number_of_jobs_alternative(100)

def run():
    compute()

if __name__ == '__main__':
    run()
