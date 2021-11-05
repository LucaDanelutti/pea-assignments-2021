from scipy.integrate import odeint
import numpy as np

def compute():
    # Generate infinitesimal generator matrix
    infinitesimal_generator = np.zeros((7, 7))
    infinitesimal_generator[0][2] = 1 / (5 * 0.75 * 0.3)
    infinitesimal_generator[0][3] = 1 / (5 * 0.25 * 0.3)
    infinitesimal_generator[0][4] = 1 / (5 * 0.7)
    infinitesimal_generator[1][2] = 1 / (10 * 0.75 * 0.3)
    infinitesimal_generator[1][3] = 1 / (10 * 0.25 * 0.3)
    infinitesimal_generator[1][4] = 1 / (10 * 0.7)
    infinitesimal_generator[2][0] = 1 / (1 * 0.4)
    infinitesimal_generator[2][1] = 1 / (1 * 0.6)
    infinitesimal_generator[3][0] = 1 / (20 * 0.4)
    infinitesimal_generator[3][1] = 1 / (20 * 0.6)
    infinitesimal_generator[4][5] = 1 / 8
    infinitesimal_generator[5][6] = 1 / 8
    infinitesimal_generator[6][0] = 1 / (8 * 0.4)
    infinitesimal_generator[6][1] = 1 / (8 * 0.6)

    for i in range(0, 7):
        infinitesimal_generator[i][i] = - sum(infinitesimal_generator[i])

    # Define pi(0) initial condition
    s0 = np.zeros((7))
    s0[0] = 0.4
    s0[1] = 0.6

    # Define differential equation
    def equation(y, x):
        dydt = np.dot(y, infinitesimal_generator)
        return dydt

    # Define u
    u = np.zeros((7))
    u[0] = 1

    # Define Q'
    infinitesimal_generator_prime = np.copy(infinitesimal_generator)
    for i in range(0, 7):
        infinitesimal_generator_prime[i][0] = 1

    # Compute stationary solution
    y_stationary = np.matmul(u, np.linalg.inv(infinitesimal_generator_prime))

    # Compute transient solution
    # Define x
    x = np.linspace(0, 1000000, 1000000)
    # Solve differential equation
    y = odeint(equation, s0, x)

    # Print probabilities using transient solution at t=100000
    print("t=1000000 probability of being computing: %f" %
          (y[999999][0] + y[999999][1]))
    print("t=1000000 probability of being WiFi: %f" %
          (y[999999][2] + y[999999][3]))
    print("t=1000000 probability of being 4G: %f" %
          (y[999999][4] + y[999999][5] + y[999999][6]))

    # Print probabilities using stationary solution
    print("Stationary probability of being computing: %f" %
          (y_stationary[0] + y_stationary[1]))
    print("Stationary probability of being WiFi: %f" %
          (y_stationary[2] + y_stationary[3]))
    print("Stationary probability of being 4G: %f" %
          (y_stationary[4] + y_stationary[5] + y_stationary[6]))

    print("Throughput: %f" % (y_stationary[6]*1*(infinitesimal_generator[6][0] +
        infinitesimal_generator[6][1]) + y_stationary[2]*1*(infinitesimal_generator[2][0] +
        infinitesimal_generator[2][1]) + y_stationary[3]*1*(infinitesimal_generator[3][0] +
        infinitesimal_generator[3][1])))

def run():
    compute()

if __name__ == '__main__':
    run()
