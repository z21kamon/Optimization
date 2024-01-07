from numpy import cos, exp, pi, abs, linspace
import matplotlib.pyplot as plt
from time import time


# characteristic function
def func(n, delta, beta, d, theta):
    phi = delta + beta * d * cos(theta)
    j = complex(0, 1)
    return sum(exp(-j * k * phi) for k in range(n))


# characteristic function derivative (for finding maximum)
def func_derivative(n, delta, beta, d, theta):
    phi = delta + beta * d * cos(theta)
    j = complex(0, 1)
    return sum(-j * k * exp(-j * k * phi) for k in range(n))


# function for plotting the delta vs modulus graph
def plot_modulus(n, beta, d, theta, num_points):
    delta_values = list(linspace(0, 2 * pi, num_points))
    modulus_values = abs([func(n, delta, beta, d, theta) for delta in delta_values])

    plt.plot(delta_values, modulus_values)
    plt.xlabel('δ')
    plt.ylabel('F(s) modulus')
    plt.grid(True)
    plt.show()


# bisection method for finding maximum
def bisection(left, right, tolerance):
    mid = (left + right) / 2

    while func_derivative(n=n, delta=mid, beta=beta, d=d, theta=theta) > tolerance:
        mid = (left + right) / 2

        if (func_derivative(n=n, delta=mid, beta=beta, d=d, theta=theta) *
                func_derivative(n=n, delta=left, beta=beta, d=d, theta=theta) < 0):
            right = mid
        else:
            left = mid

    return mid


n = 6
beta = 20 * pi
d = 1 / 20
theta = pi / 3

# solve the problem
start_time = time()
plot_modulus(n=n, beta=beta, d=d, theta=theta, num_points=100)
answer = bisection(left=4, right=5, tolerance=10 ** -7)
maximum = abs(func(n=n, delta=answer, beta=beta, d=d, theta=theta))

print(f"Maximum of modulus of F_s: {maximum}\nDelta, which yields it: {answer}")
print(f"Total program execution time: {(time() - start_time)} seconds")
