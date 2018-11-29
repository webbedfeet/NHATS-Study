#!/usr/bin/env python
# coding: utf-8

import numpy as np
import scipy as sp
import pandas as pd 
import seaborn as sns 
from glob import glob
from functools import reduce

# Importing the Datasets 

df1 = pd.read_csv('Round1.csv')
df2 = pd.read_csv('Round2.csv')
df3 = pd.read_csv('Round3.csv')
df4 = pd.read_csv('Round4.csv')
df5 = pd.read_csv('Round5.csv')
df6 = pd.read_csv('Round6.csv')
df7 = pd.read_csv('Round7.csv')



# Merging the Datasets 

mergedset1 = pd.merge(df1, df2, on='spid',how='left')
mergedset2 = pd.merge(mergedset1,df3,on='spid',how='left')
mergedset3 = pd.merge(mergedset2,df4,on='spid',how='left')
mergedset4 = pd.merge(mergedset3,df5,on='spid',how='left')
mergedset5 = pd.merge(mergedset4,df6,on='spid',how='left')
mergedset_final = pd.merge(mergedset5,df7,on='spid',how='left')

#AD# The above code can be summarized into one command, below
#AD# mergedset_final = reduce(lambda x,y: pd.merge(x, y, on='spid', how = 'left'), 
#AD#        [pd.read_csv(f) for f in glob('Round*.csv')])

# Excluding Patients Without Arthritis 

total_patients_arthritis = mergedset_final[mergedset_final.hc1disescn4 == '1 YES']

#AD# total_patients_arthritis = mergedset_final.query("hc1disescn4=='1 YES')

# Converting the Age Variable from String to Int 

conditions = [(total_patients_arthritis['r1d2intvrage'] == '1 - 65-69') , (total_patients_arthritis['r1d2intvrage'] == '2 - 70-74'),
    (total_patients_arthritis['r1d2intvrage'] == '3 - 75-79') , (total_patients_arthritis['r1d2intvrage'] == '4 - 80-84'),
    (total_patients_arthritis['r1d2intvrage'] == '5 - 85-89'), (total_patients_arthritis['r1d2intvrage'] == '6 - 90 +')]
choices = [1,2,3,4,5,6]
total_patients_arthritis['Age'] = np.select(conditions, choices)

#AD# you could do
#AD# total_patients_arthritis['r1d2intvrage'] = pd.Series(list(map(lambda x: int(x[0]), total_patients_arthritis['r1d2intvrage'])))

# Creating a Variable for Joint Replacement (Hip and/or Knee) Status

total_patients_arthritis['THR'] = np.where(total_patients_arthritis['hc1hipsurg'] == '1 YES', 1, 0)
total_patients_arthritis['TKR'] = np.where(total_patients_arthritis['hc1kneesurg'] == '1 YES', 1, 0) 
total_patients_arthritis['TJR'] = np.where(total_patients_arthritis['THR']+total_patients_arthritis['TKR'] >= 1, 'Yes', 'No')

#AD# total_patients_arthritis['TJR'] = pd.Series(np.where((total_patients_arthritis.THR == 1) | (total_patients_arthritis['TKR'] ==1), 'Yes','No'), dtype = 'category')

# Removing the Missing Imputed Income Values Round 1 and Round 3 from the Set

total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia1toincim1 != '-1 Inapplicable']
total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia1toincim1 != '-9 Missing']
total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia1toincim1 != '.']

total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia3toincim1 != '-1 Inapplicable']
total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia3toincim1 != '-9 Missing']
total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia3toincim1 != '.']

#AD# Denote these as missing, rather than getting rid of them
#AD# missvals = ['-1 Inapplicable','-9 Missing','.']
#AD# total_patients_arthritis.ia1toincim1[total_patients_arthritis.ia1toincim1.isin(missvals)] = np.nan
#AD# total_patients_arthritis.ia3toincim1[total_patients_arthritis.ia3toincim1.isin(missvals)] = np.nan


# Converting the Imputed Income Values Round 1 - Round 3 from pd.Series to float
#AD# Why? Columns in a DataFrame are always pd.Series, but what's important is the data type. You can see the data types for each
#AD# column by total_patients_arthritis.dtypes

total_patients_arthritis['ia1toincim1'] = total_patients_arthritis['ia1toincim1'].astype(float)
total_patients_arthritis['ia1toincim2'] = total_patients_arthritis['ia1toincim2'].astype(float)
total_patients_arthritis['ia1toincim3'] = total_patients_arthritis['ia1toincim3'].astype(float)
total_patients_arthritis['ia1toincim4'] = total_patients_arthritis['ia1toincim4'].astype(float)
total_patients_arthritis['ia1toincim5'] = total_patients_arthritis['ia1toincim5'].astype(float)

total_patients_arthritis['ia3toincim1'] = total_patients_arthritis['ia3toincim1'].astype(float)
total_patients_arthritis['ia3toincim2'] = total_patients_arthritis['ia3toincim2'].astype(float)
total_patients_arthritis['ia3toincim3'] = total_patients_arthritis['ia3toincim3'].astype(float)
total_patients_arthritis['ia3toincim4'] = total_patients_arthritis['ia3toincim4'].astype(float)
total_patients_arthritis['ia3toincim5'] = total_patients_arthritis['ia3toincim5'].astype(float)

# Computing the Average Imputed Income for Round 1

total_patients_arthritis['R1avg_income1-5'] = (total_patients_arthritis['ia1toincim1']+total_patients_arthritis['ia1toincim2']+total_patients_arthritis['ia1toincim3']+total_patients_arthritis['ia1toincim4']+total_patients_arthritis['ia1toincim5'])/5


#AD# total_patients_arthritis['R1avg_income1-5'] = total_patients_arthritis.eval('(ia1toincim1+ia1toincim2+ia1toincim3+ia1toincim4+ia1toincim5)/5')
#AD# OR
#AD# total_patients_arthritis['R1avg_income1-5'] = total_patients_arthritis.loc[:,'ia1toincim1':'ia1toincim5'].mean(axis=1)
#AD# OR
#AD# total_patients_arthritis['R1avg_income1-5] = (total_patients_arthritis.loc[:,['spid','ia1toincim1','ia1toincim2','ia1toincim3','ia1toincim4','ia1toincim5']].
#AD#     melt(id_vars = 'id').
#AD#     groupby(['id']).mean())


# Computing the Average Imputed Income for Round 3 

total_patients_arthritis['R3avg_income1-5'] = (total_patients_arthritis['ia3toincim1']+total_patients_arthritis['ia3toincim2']+total_patients_arthritis['ia3toincim3']+total_patients_arthritis['ia3toincim4']+total_patients_arthritis['ia3toincim5'])/5

# Computing the Change in Income Between Round 1 and Round 3  

total_patients_arthritis['changeR1R3'] = total_patients_arthritis['R1avg_income1-5']-total_patients_arthritis['R3avg_income1-5']

# Excluding the top and bottom 1% of change in income values 

total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.changeR1R3 <200000]
total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.changeR1R3 >-200000]

#AD# Don't hard-code these numbers
#AD# lower = total_patients_arthritis.changeR1R3.quantile(0.01)
#AD# upper = total_patients_arthritis.changeR1R3.quantile(0.99)
#AD# indic = (total_patients_arthritis.changeR1R3 <= lower) | (total_patients_arthritis.changeR1R3 >= upper)
#AD# total_patients_arthritis.changeR1R3[indic] = np.nan


# Separating Individuals with TJR from those Without 

total_patients_arthritis_TJR = total_patients_arthritis[total_patients_arthritis.TJR == 'Yes']
total_patients_arthritis_NoTJR = total_patients_arthritis[total_patients_arthritis.TJR == 'No']

########################################
# Starting the Analysis Phase 
########################################

# Wilcoxon Signed Rank Test - Is changeR1R3 for TJR significantly different from 0? 
sp.stats.wilcoxon(total_patients_arthritis_TJR['changeR1R3'], zero_method='wilcox', correction=False)


# Wilcoxon Signed Rank Test - Is changeR1R3 for NoTJR significantly different from 0? 
sp.stats.wilcoxon(total_patients_arthritis_NoTJR['changeR1R3'], zero_method='wilcox', correction=False)


# Removing the Missing Imputed Income Values from the Set

#AD# See earlier for simpler code
total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia1toincim1 != '-1 Inapplicable']
total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia1toincim1 != '-9 Missing']
total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia1toincim1 != '.']

total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia3toincim1 != '-1 Inapplicable']
total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia3toincim1 != '-9 Missing']
total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia3toincim1 != '.']

total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia5toincim1 != '-1 Inapplicable']
total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia5toincim1 != '-9 Missing']
total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia5toincim1 != '.']

total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia7toincim1 != '-1 Inapplicable']
total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia7toincim1 != '-9 Missing']
total_patients_arthritis = total_patients_arthritis[total_patients_arthritis.ia7toincim1 != '.']

