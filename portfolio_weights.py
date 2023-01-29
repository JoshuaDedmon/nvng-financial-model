import yfinance as yf
from scipy.optimize import minimize
import numpy as np

goldilocks_stocks = \
["DOV", "HSY", "OKE", "META", "FSLR", "IPG", "UNP", "CL", "FMC", "AVB"]

data = yf.download(goldilocks_stocks, start = "2021-01-01", \
end = "2021-12-31")["Adj Close"]

returns = data.pct_change()

# Optimizing function
def optimize_portfolio(weights, alpha):
    portfolio_return = np.sum(returns.mean() * weights) * 252 * 0.5
    portfolio_volatility = \
    np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    sharpe_ratio = (portfolio_return - alpha) / portfolio_volatility
    RAR = (portfolio_return + 0.5 * sharpe_ratio) * -1
    return RAR

# Constraints
def constraints(weights):
    avg_return = returns.mean().mean()
    for i, ticker in enumerate(goldilocks_stocks):
        if returns.mean()[i] > avg_return:
            min_weight = 0.15
            weights[i] = max(weights[i], min_weight)
        else:
            max_weight = 0.05
            weights[i] = min(weights[i], max_weight)
    for i in range(len(weights)):
        weights[i] = min(weights[i], 0.3)
    return [np.sum(weights) - 1]

# Bootstrapping
n_samples = 10

optimal_weights_array = np.zeros((n_samples, len(goldilocks_stocks)))

risk_free_rate = 0.00001

for i in range(n_samples):
    sample_returns = returns.sample(n=len(returns), replace=True)

    # Optimizing weights
    bounds = [(0, 1) for i in range(len(goldilocks_stocks))]
    initial_guess = \
    np.random.dirichlet(np.ones(len(goldilocks_stocks)),size = 1)
    initial_guess = initial_guess.flatten()
    con = {"type": "eq", "fun": constraints}
    optimal_weights = minimize(optimize_portfolio, initial_guess, \
    args = (risk_free_rate,), bounds = bounds, constraints = con)
    optimal_weights_array[i, :] = optimal_weights.x

mean_weights = np.mean(optimal_weights_array, axis = 0)
std_weights = np.std(optimal_weights_array, axis = 0)


for i, ticker in enumerate(goldilocks_stocks):
    print(f"{ticker}: Advised Weight: {mean_weights[i]:.4f}")
