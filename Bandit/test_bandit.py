import matplotlib.pyplot as plt
from bandit import run_game


def test_results():
    iterations = 1000
    means = [1, 2, 5]
    x_range = range(iterations)

    # Plot average reward
    for e in [0.2, 0.1, 0.01, 0.05]:
        avg_reward= run_game(iterations, e, "Normal", *means)
        plt.plot(x_range, avg_reward, label=e)
    plt.legend()
    plt.title("Average reward for Normal strategy")
    plt.show()

    for strategy in ["Optimistic", "Confidence", "Bayesian"]:
        avg_reward = run_game(iterations, e, strategy, *means)
        plt.plot(x_range, avg_reward, label=strategy)
    plt.legend()
    plt.title("Average reward for Optimistic, Confidence and Bayesian strategies")
    plt.show()

    for strategy in ["Normal", "Bayesian"]:
        avg_reward = run_game(iterations, e, strategy, *means)
        plt.plot(x_range, avg_reward, label=strategy)
    plt.legend()
    plt.title("Normal vs Bayesian")
    plt.show()

test_results()