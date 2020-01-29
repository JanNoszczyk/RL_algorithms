import numpy as np
from math import sqrt, log
from abc import abstractmethod, ABC


class Bandit(ABC):
    @abstractmethod
    def __init__(self, true_mean):
        self.true_mean = true_mean
        self.N = 0
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
        super().__init__(true_mean)
        self.mean = 0


class OptimisticBandit(Bandit):
    def __init__(self, true_mean, init_mean):
        super().__init__(true_mean)
        self.mean = init_mean


class BayesianBandit:
    def __init__(self, true_mean):
        self.true_mean = true_mean
        # The bandits mean is itself a random variable now so use sample to get mean
        # Assume mean normally distributed with (0, 1)
        self.tau = 1
        self.m = 0
        self.lam = 1
        self.sum_x = 0

    def play(self):
        # We now sample the likelihood
        x = np.random.randn()/sqrt(self.tau) + self.true_mean
        # Calculate new bandit mean after drawing new sample
        # Note that m0 = 0 and lam0 = 1 and tau = 1
        # lambda = N , so update lambda by extending N by 1 sample
        self.lam += 1
        self.sum_x += x
        self.m = self.tau*self.sum_x/self.lam
        return x

    def sample(self):
        # We now sample posterior
        return np.random.randn()/sqrt(self.lam) + self.m


def run_game(iterations, epsilon, strategy="Normal", *means):
    if strategy == "Bayesian":
        bandits = [BayesianBandit(m) for m in means]
    elif strategy == "Optimistic" or strategy == "Confidence":
        bandits = [OptimisticBandit(m, 1.2*m) for m in means]
    else:
        bandits = [NormalBandit(m) for m in means]

    average_reward, bandit_means = [], []
    for i in range(iterations):
        if strategy == "Bayesian":
            sampled_posteriors = [(b, b.sample()) for b in bandits]
            bandit = sorted(sampled_posteriors, key=lambda k: k[1])[-1][0]
        elif strategy == "Confidence":
            # Add small number to denominator to avoid zero division error
            bounds = [(b, b.mean + sqrt(2*log(i+1)/(b.N+0.000001))) for b in bandits]
            bandit = sorted(bounds, key=lambda k: k[1])[-1][0]
        elif strategy == "Optimistic":
            bandit = sorted(bandits, key=lambda k: k.mean)[-1]
        else:
            # random() generates a sample from (0, 1) continuous distribution, ie a random probability
            p = np.random.random()
            if i > 0: epsilon = 1/i
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

    return average_reward

