#%% -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 13:23:38 2020
@author: Robbie Cunningham
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
pd.options.display.width = 180
pd.options.display.max_columns = 60
pd.options.display.max_rows = 100
from matplotlib.dates import DateFormatter, DayLocator



spop = pd.read_pickle('spop.pkl')
pop = spop.to_dict()
df = pd.read_json('https://covidtracking.com/api/states/daily')
df.date = pd.to_datetime(df.date, format='%Y%m%d')
#%%

fig = plt.gcf()
fig.clear()

# scale = {'death':100,'positive':1}

scale = {'positive':1}

for metric in list(scale.keys()):
    data = pd.merge(df[['date','state',metric]],df.groupby('state').death.sum().rename('total'),left_on = 'state', right_on = 'state').sort_values(by='total')
    data = data.pivot('date','state',metric) #.dropna()
    data = data[list(pop.keys())]
    data = data.apply(lambda x: scale[metric]*x/pop[x.name])
    data = data.assign(m=data.sum(axis=1)).sort_values('m').drop('m', axis=1)
    data = data.append(data.sum().rename('sum')).sort_values('sum',axis=1,ascending=False).drop('sum')
    ax = sns.lineplot(data=data, palette='Spectral')
    ax.legend(ncol=2)
    plt.title(f'Covid {metric.title()}s per Capita per State, 2020')
    plt.ylabel('Percentage of total Population')
    plt.xlabel('Date')
    ax.xaxis.set_major_formatter(DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(DayLocator(interval=7))
    plt.xticks(fontsize=6)
    fig.autofmt_xdate()
    
    







