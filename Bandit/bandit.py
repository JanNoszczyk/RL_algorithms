import numpy as np
import matplotlib.pyplot as plt


class Bandit:
    def __init__(self, true_mean):
        self.true_mean = true_mean
        self.mean = 0
        self.N = 0

    def play(self):
        # randn() returns a gaussian N(0, 1), change mean by adding it to result
        x = np.random.randn() + self.true_mean
        # Calculate new bandit mean after drawing new sample
        self.N += 1
        self.mean = self.mean * (self.N - 1) / self.N + x * 1 / self.N
        return x


def run_game(iterations, epsilon, *means):
    bandits = [Bandit(m) for m in means]
    max_bandit = bandits[0]
    average_reward, bandit_means = [], []
    for i in range(iterations):
        # random() generates a sample from (0, 1) continuous distribution, ie a random probability
        p = np.random.random()
        if p < epsilon:
            # Explore, choose a random bandit, without getting a reward
            bandit = bandits[np.random.randint(0, len(bandits))]
        else:
            # Exploit, get reward from currently best bandit
            bandit = max_bandit

        x = bandit.play()
        # Update best bandit if its mean exceeds current max
        if bandit.mean > max_bandit.mean:
            max_bandit = bandit

        # track average reward and bandit means for plotting
        if i > 0:
            average_reward.append((average_reward[-1] + x)/2)
        else:
            average_reward.append(x)
        bandit_means.append([b.mean for b in bandits])

    # Plot bandit means
    N_b = len(bandits)
    x_range = range(iterations)
    bandit_means = list(zip(*bandit_means))
    for j in range(N_b):
        plt.subplot(N_b, 1, j+1)
        plt.plot(x_range, bandit_means[j])
        plt.title("Bandit {}".format(j+1))
    plt.show()

    # Plot average reward
    plt.plot(x_range, average_reward)
    plt.title("Average reward")
    plt.show()

run_game(300, 0.1, 1, 2, 5)