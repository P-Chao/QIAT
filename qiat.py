import tushare as ts
import matplotlib.pyplot as plt

df = ts.get_hist_data('sh', start = '2016-01-01')
df.to_excel('stock_sh.xlsx')
df.close.plot()
ax = plt.gca()
ax.invert_xaxis()
plt.show()