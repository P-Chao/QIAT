import numpy as np
import matplotlib.pyplot as plt
from types import SimpleNamespace


class Option:
    def __init__(self, name, price):
        self.name = name
        self.stock = name
        self.price = price
        self.stock, _, self.exercise_price = name.split(' ')
        self.exercise_price = float(self.exercise_price)


def calc_option_earnings(tic_price, option, operation='long'):

    # exercise inner value
    value_option = tic_price
    if 'call' in option.name.lower():
        value_option = np.maximum(0, tic_price - option.exercise_price)
    if 'put' in option.name.lower():
        value_option = np.maximum(0, option.exercise_price - tic_price)
    if 'sell' in operation.lower() or 'short' in operation.lower():
        value_option = -value_option

    earnings = value_option - option.price

    return earnings


def test_straddle():
    tic_price = np.arange(0, 100, 0.01)

    option_call = Option("JD CALL 59", 4.40)
    option_put = Option('JD PUT 59', 1.67)

    long_call = calc_option_earnings(tic_price, option_call, 'LONG')
    long_put = calc_option_earnings(tic_price, option_put, 'LONG')

    plt.figure()
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0.1, hspace=0.0)
    plt.subplot(1, 2, 1)
    plt.plot(tic_price, long_call + long_put, label='total')
    plt.plot(tic_price, long_call, linestyle='--', label='long call')
    plt.plot(tic_price, long_put, linestyle='-.', label='long put')
    plt.legend()
    plt.title('LONG STRADDLE')
    plt.xlabel('stock price at option expire')
    plt.ylabel('earnings')
    plt.grid(axis='y', linestyle=':')


def test_strangle():
    tic_price = np.arange(0, 100, 0.01)

    option_call = Option("JD CALL 65", 1.45)
    option_put = Option('JD PUT 55', 0.58)

    long_call = calc_option_earnings(tic_price, option_call, 'LONG')
    long_put = calc_option_earnings(tic_price, option_put, 'LONG')

    plt.figure()
    plt.plot(tic_price, long_call + long_put, label='total')
    plt.plot(tic_price, long_call, linestyle='--', label='long call')
    plt.plot(tic_price, long_put, linestyle='-.', label='long put')
    plt.legend()
    plt.title('LONG STRADDLE')
    plt.xlabel('stock price at option expire')
    plt.ylabel('earnings')
    plt.grid(axis='y', linestyle=':')


if __name__ == "__main__":
    test_straddle()
    test_strangle()
