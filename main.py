# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 13:23:38 2020
@author: Robbie Cunningham
"""

import matplotlib.pyplot as plt
import pandas as pd
pd.options.display.width = 180
pd.options.display.max_columns = 30
pd.options.display.max_rows = 100

plt.gcf().clear()

spop = pd.read_pickle('spop.pkl')
pop = spop.to_dict()
#%%



df = pd.read_json('https://covidtracking.com/api/states/daily')

# states = ['OR', 'CA', 'NY']
df = df[df.state.isin(list(pop.keys()))]
df.date = pd.to_datetime(df.date, format='%Y%m%d')
df.sort_values(by = 'date', inplace=True)
df.set_index('date', drop=True, inplace=True)

print(df.head())
gb = df.groupby('state')



for name,g in gb.__iter__():
    (g.death.rename(name)/pop[name]).plot()
plt.title('Covid Death Per Capita Per State')
plt.legend()



