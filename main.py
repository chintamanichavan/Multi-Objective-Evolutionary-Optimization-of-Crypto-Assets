import numpy as np
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

# Define your problem class
class CryptoProblem:
    def __init__(self, returns, risks, n_assets):
        self.returns = returns
        self.risks = risks
        self.n_assets = n_assets

    def _evaluate(self, X, out, *args, **kwargs):
        # Objective 1: maximize return
        out["F"][:, 0] = -np.sum(X * self.returns, axis=1)

        # Objective 2: minimize risk
        out["F"][:, 1] = np.sum(X * self.risks, axis=1)

        # Ensure diversification: each solution should hold at least n assets
        out["G"] = self.n_assets - np.sum(X > 0.01, axis=1)

# Define problem with hypothetical returns and risks
problem = CryptoProblem(returns=np.random.rand(100), risks=np.random.rand(100), n_assets=10)

algorithm = NSGA2(pop_size=100)

res = minimize(problem, algorithm, ("n_gen", 100), verbose=True)

# Plotting the solutions using Plotly.js
import plotly.graph_objects as go

f1 = [i[0] for i in res.F]
f2 = [i[1] for i in res.F]

fig = go.Figure(data=go.Scatter(x=f1, y=f2, mode='markers'))

fig.show()
