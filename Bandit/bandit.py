import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, log
from abc import abstractmethod, ABC

class Bandit(ABC):
    @abstractmethod
    def __init__(self, true_mean, init_mean=None):
        pass

    def play(self):
        # randn() returns a gaussian N(0, 1), change mean by adding it to result
        x = np.random.randn() + self.true_mean
        # Calculate new bandit mean after drawing new sample
        self.N += 1
        self.mean = self.mean * (self.N - 1) / self.N + x * 1 / self.N
        return x


class NormalBandit(Bandit):
    def __init__(self, true_mean):
        self.true_mean = true_mean
        self.mean = 0
        self.N = 0


class OptimisticBandit(Bandit):
    def __init__(self, true_mean, init_mean):
        self.true_mean = true_mean
        self.mean = init_mean
        self.N = 0


def run_game(iterations, epsilon, strategy="Normal", *means):
    if strategy == "Optimistic" or strategy == "Confidence":
        bandits = [OptimisticBandit(m, 1.2*m) for m in means]
    else:
        bandits = [NormalBandit(m) for m in means]

    average_reward, bandit_means = [], []
    for i in range(iterations):
        if strategy == "Confidence":
            # Add small number to denominator to avoid zero division error
            bounds = [(b, b.mean + sqrt(2*log(i+1)/(b.N+0.000001))) for b in bandits]
            bandit = sorted(bounds, key=lambda k: k[1])[-1][0]
        elif strategy == "Optimistic":
            bandit = sorted(bandits, key=lambda k: k.mean)[-1]
        else:
            # random() generates a sample from (0, 1) continuous distribution, ie a random probability
            p = np.random.random()
            if p > epsilon:
                # Exploit, get reward from currently best bandit
                bandit = sorted(bandits, key=lambda k: k.mean)[-1]
            else:
                # Explore, choose a random bandit, without getting a reward
                bandit = bandits[np.random.randint(0, len(bandits))]

        x = bandit.play()

        # track average reward and bandit means for plotting
        if i > 0:
            new_avg = average_reward[-1]*(len(average_reward))/(len(average_reward)+1) + x/(len(average_reward)+1)
            average_reward.append(new_avg)
        else:
            average_reward.append(x)
        bandit_means.append([b.mean for b in bandits])

    return average_reward, bandit_means

def test_results():
    iterations = 1000
    epsilon = 0.1
    means = [1, 2, 5]
    average_reward, bandit_means = run_game(iterations, epsilon, *means)

    # # Plot bandit means
    # N_b = len(means)
    x_range = range(iterations)
    # bandit_means = list(zip(*bandit_means))
    # for j in range(N_b):
    #     plt.subplot(N_b, 1, j+1)
    #     plt.plot(x_range, bandit_means[j])
    #     plt.title("Bandit {}".format(j+1))
    # plt.show()

    # Plot average reward
    for e in [0.2, 0.1, 0.01, 0.05]:
        avg_reward, _ = run_game(iterations, e, "Normal", *means)
        plt.plot(x_range, avg_reward, label=e)
    plt.legend()
    plt.title("Average reward for Normal strategy")
    plt.show()

    for strategy in ["Optimistic", "Confidence"]:
        avg_reward, _ = run_game(iterations, e, strategy, *means)
        plt.plot(x_range, avg_reward, label=strategy)
    plt.legend()
    plt.title("Average reward for Optimistic and Confidence strategies")
    plt.show()


test_results()