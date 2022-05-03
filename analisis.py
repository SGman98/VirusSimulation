import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# use different methods to find the curve


def linear(list_, x0=0):
    x = [i for i in range(len(list_))]
    y = list_
    m, b = np.polyfit(x, y, 1)
    # print function
    print(f'Linear function:\n\tf(x) = {round(m, 4)}x + {round(b, 4)}')
    if x0 != 0:
        print(f'f({x0}) = {round(m * x0 + b, 4)}')
    return [m * i + b for i in range(len(list_))]


def quadratic(list_, x0=0):
    x = [i for i in range(len(list_))]
    y = list_
    m, b, c = np.polyfit(x, y, 2)
    # print function
    print(f'Quadratic function:\n\tf(x) = {round(m, 4)}x^2 + {round(b, 4)}x + {round(c, 4)}')

    if x0 != 0:
        print(f'f({x0}) = {round(m * x0**2 + b * x0 + c, 4)}')
    return [m * i ** 2 + b * i + c for i in range(len(list_))]


def poly_newton(list_, degree, x0=0):
    x = [i for i in range(len(list_))]
    y = list_
    # create a list of the polynomial coefficients
    coeffs = np.polyfit(x, y, degree)
    # create a function from the coefficients
    poly = np.poly1d(coeffs)
    # print function
    print(f'Polynomial function degree {degree}:\n\tf(x) = ', end='')
    for i in range(len(poly.coeffs)):
        print(f'{round(poly.coeffs[i], 4)}x^{degree - i}', end='')
        if i != len(coeffs) - 1:
            print(' + ', end='')
    print()
    if x0 != 0:
        print(f'f({x0}) = {round(poly(x0), 4)}')
    return poly(x)


# use iteration to find the poly_newton degree with minimum error
def poly_newton_optimal(list_):
    x = [i for i in range(len(list_))]
    y = list_
    # create a list of the polynomial coefficients
    coeffs = np.polyfit(x, y, 1)

    # create a function from the coefficients
    poly = np.poly1d(coeffs)

    # loop trough all the degrees and find the minimum error
    min_error = float('inf')
    min_degree = 0
    for i in range(2, 50):
        # create a function from the coefficients
        poly = np.poly1d(np.polyfit(x, y, i))
        # calculate the error
        error = np.sum(np.abs(poly(x) - y))
        # if the error is smaller than the current minimum, save the degree and the error
        if error < min_error:
            min_error = error
            min_degree = i

    # print the degree and the error
    print(f'Polynomial function degree {min_degree} with minimum error: {min_error}')
    return min_degree


def graph(list_, name):
    data_x = [x for x in range(len(list_))]
    plt.plot(data_x, list_, 'r-', label=name)
    plt.plot(data_x, linear(list_), 'b-', label='linear')
    plt.plot(data_x, quadratic(list_), 'g-', label='quadratic')
    degree = poly_newton_optimal(list_)
    plt.plot(data_x, poly_newton(list_, degree), 'k-', label=f'poly_newton_{degree}')
    plt.legend()


def print_data(list_, num):
    linear(list_, num)
    quadratic(list_, num)
    degree = poly_newton_optimal(list_)
    poly_newton(list_, degree, num)


def data_analisis(num):
    with open('data.csv', 'r') as f:
        data = f.readline().split(',')
        infected = [int(x) for x in data]
        data = f.readline().split(',')
        dead = [int(x) for x in data]

    # infected
    print('Infected')
    print_data(infected, num)
    print()
    # dead
    print('Dead')
    print_data(dead, num)

    # create a graph with infected, dead and suceptible
    # suceptible = 500 - infected - dead
    suceptible = [500 - i - d for i, d in zip(infected, dead)]

    # suceptible in blue, infected in red, dead in black

    plt.plot(suceptible, 'b-', label='healthy')
    plt.plot(infected, 'r-', label='infected')
    plt.plot(dead, 'k-', label='dead')
    plt.legend()
    plt.show()


def data_analisis_graph():
    with open('data.csv', 'r') as f:
        data = f.readline().split(',')
        infected = [int(x) for x in data]
        data = f.readline().split(',')
        dead = [int(x) for x in data]

    # Create 2 subplots 1 for infected and 1 for dead
    fig, axs = plt.subplots(2, 1)
    # infected
    plt.subplot(2, 1, 1)
    print('Infected')
    graph(infected, 'infected')
    print()
    # dead
    print('Dead')
    plt.subplot(2, 1, 2)
    graph(dead, 'dead')
    # pause
    plt.show()
    plt.pause(0.001)


if __name__ == '__main__':
    data_analisis(600)
    # data_analisis_graph()
