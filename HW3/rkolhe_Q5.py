#Question 5
#Unity- rkolhe

import pandas as pd
import collections
from matplotlib_venn import venn3
import matplotlib.pyplot as plt

#read csv file
df = pd.read_csv('Tor_query_EXPORT.csv')


#Top 5 countries
top_5_cont = [country[0] for country in collections.Counter(df['Country Code']).most_common(5)]
print('\nTop 5 countries-')
print(top_5_cont)


#Top 5 bandwidths
most_common = df.mask(df['ConsensusBandwidth'].eq('None').fillna(0))
most_common['ConsensusBandwidth'] = pd.to_numeric(most_common['ConsensusBandwidth'])
most_common = most_common.nlargest(5, columns = 'ConsensusBandwidth')
most_common = most_common[['Router Name','Country Code','Hostname','IP Address','ConsensusBandwidth']]
print('\n Top 5 bandwidths-')
print(f'{most_common}')


guard = df['Flag - Guard']
guard = guard.fillna(0)
guard_ids_1 = set(df.index[guard == 1])

exit = df['Flag - Exit']
exit = exit.fillna(0)
exit_ids_1= set(df.index[exit == 1])

guard_ids_0 = set(df.index[guard == 0])
exit_ids_0= set(df.index[exit == 0])
mid_ids = set()
mid_ids = guard_ids_0.intersection(exit_ids_0)

guard_only = guard_ids_1.difference(exit_ids_1)
exit_only = exit_ids_1.difference(guard_ids_1)

total_exit = len(exit_only)
total_guard = len(guard_only)
total_mid = len(mid_ids)

bandwidth = df['ConsensusBandwidth']
bandwidth = [0 if val == 'None' else int(val) for val in bandwidth]


guard_band = 0
for index in guard_only:
    guard_band += bandwidth[index]

exit_band = 0
for index in exit_only:
    exit_band += bandwidth[index]
    
mid_band = 0	
for index in mid_ids:
    mid_band += bandwidth[index]

print('\nCounts for each relay type')
print(f'Guard: {total_guard}, Mid: {total_mid}, Exit: {total_exit}')
print('\nCumulative bandwidhts')
print(f'Guard Bandwidth: {guard_band}, Mid Bandwidth: {mid_band}, Exit Bandwidth: {exit_band}')

venn3([guard_ids_1, exit_ids_1, mid_ids], ('Guard', 'Exit', 'Mid'))
plt.show()