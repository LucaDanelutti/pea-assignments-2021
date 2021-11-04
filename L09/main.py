from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def compute(t):
    # RAID system parameters
    l_fail = 1 / 100
    l_recover = 1 / 5
    l_reconstruction = 1 / 15

    # Generate infinitesimal generator matrix
    infinitesimal_generator = np.zeros((4, 4))
    infinitesimal_generator[0][1] = l_fail
    infinitesimal_generator[0][2] = l_fail
    infinitesimal_generator[1][3] = l_fail
    infinitesimal_generator[2][3] = l_fail
    infinitesimal_generator[1][0] = l_recover
    infinitesimal_generator[2][0] = l_recover
    infinitesimal_generator[3][0] = l_reconstruction

    infinitesimal_generator[0][0] = - sum(infinitesimal_generator[0])
    infinitesimal_generator[1][1] = - sum(infinitesimal_generator[1])
    infinitesimal_generator[2][2] = - sum(infinitesimal_generator[2])
    infinitesimal_generator[3][3] = - sum(infinitesimal_generator[3])

    # Define pi(0) initial condition
    s0 = np.zeros((4))
    s0[0] = 1

    # Define differential equation
    def equation(y, x):
        dydt = np.dot(y, infinitesimal_generator)
        return dydt

    # Define x
    x = np.linspace(0, t, t)
    # Solve differential equation
    y = odeint(equation, s0, x)

    # Print results
    print("Time %d probability of normal operation: %f" % (t, y[t-1][0]))
    print("Time %d probability of hd1 under repair: %f" % (t, y[t-1][1]))
    print("Time %d probability of hd2 under repair: %f" % (t, y[t-1][2]))
    print("Time %d probability of fault state: %f" % (t, y[t-1][3]))

    # Plot results
    plt.plot(x, y)
    plt.grid()
    plt.xlabel('time')
    plt.ylabel('y(t)')
    plt.legend(['Normal operation', 'First hd KO', 'Second hd KO', 'RAID KO'])
    plt.show()

def run():
    compute(10000)

if __name__ == '__main__':
    run()
