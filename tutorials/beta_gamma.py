import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta, gamma




# beta_pdf = beta.pdf(x=np.linspace(0, 1, 100), a=2, b=5, loc=0)
# ax0 = plt.plot(beta_pdf)

# beta_rvs = beta.rvs(a=2, b=5, loc=0, scale=200, size=25000)
# plt.hist(beta_rvs, bins=100)

_gamma = gamma.pdf(np.linspace(0, 100, 100), 2, 5, 10)
ax0 = plt.plot(_gamma)

plt.show()





