import pandas as pd
import numpy as np
import sys

filepath = sys.argv[1]
output_filepath = sys.argv[2]

df_make = pd.read_csv(filepath, dtype=object)

df_make['Issue Date'] = pd.to_datetime(df_make['Issue Date'])

# only keep records with the right expiry dates
df_make = df_make.loc[df_make['Plate Expiry Date'].str.len() == 8]

# extract year and month 
df_make['year'] = df_make['Plate Expiry Date'].str[:4].astype('int')
df_make['month'] = df_make['Plate Expiry Date'].str[4:6].astype('int')
df_make['day'] = 1

# make sure the date is within a realistic timeframe
df_make = df_make.loc[(df_make['year'].between(1990, 2020, inclusive=True))&(df_make['month'].between(1, 12, inclusive=True))]

# recreate the plate expiration date field
df_make['plate_expiry_date'] = pd.to_datetime(df_make[['year', 'month', 'day']])

# creating an "instate" field
df_make['instate'] = 0 
df_make.loc[df_make['RP State Plate'] == 'CA', 'instate'] = 1

# create an "expired" field
df_make['expired'] = 0
df_make.loc[(df_make['plate_expiry_date'] < df_make['Issue Date']), 'expired'] = 1

# bin the colors into top 10
top_colors = df_make['Color'].value_counts(normalize = True).cumsum()[:10]
df_make['Color'] = np.where(df_make['Color'].isin(top_colors.index), df_make['Color'], 'Other')

# bin the styles into top 5
top_style = df_make['Body Style'].value_counts(normalize = True).cumsum()[:5]
df_make['Body Style'] = np.where(df_make['Body Style'].isin(top_style.index), df_make['Body Style'], 'Other')

conditions = [
    (df_make['Fine amount'].astype('float').between(0,50)),
    (df_make['Fine amount'].astype('float').between(50,100))]
choices = ['low', 'medium']
df_make['fine_cat'] = np.select(conditions, choices, default='big')

# get num of days between ticket issued and plate expiration
df_make['days_between_issue_expired'] = (df_make['plate_expiry_date'] - df_make['Issue Date']).dt.days

# creating a categorical variable for issue time
conditions = [
    (df_make['Issue time'].astype('float').between(0,600)), # early hours
    (df_make['Issue time'].astype('float').between(600,1200)), # morning
    (df_make['Issue time'].astype('float').between(1200,1800)), # afternoon
]
choices = ['early_hours', 'morning', 'afternoon']
df_make['issue_time_cat'] = np.select(conditions, choices, default='night')

df_make['Fine amount'] = df_make['Fine amount'].astype('float')
df_make['Fine amount'] = df_make['Fine amount'].fillna(value=0)

keep_var = ['Body Style', 'Color', 'Fine amount', 'instate', 'expired',
       'fine_cat', 'issue_time_cat',
       'days_between_issue_expired']

df_make = df_make[keep_var]

df_make_model = pd.get_dummies(df_make)

vars_needed = ['Body Style_CM', 'Body Style_Other',
'Body Style_PA', 'Body Style_PU', 'Body Style_TK', 'Body Style_VN',
'Color_BK', 'Color_BL', 'Color_GN', 'Color_GO', 'Color_GY', 'Color_MR',
'Color_Other', 'Color_RD', 'Color_SL', 'Color_WH', 'Color_WT',
'fine_cat_big', 'fine_cat_low', 'fine_cat_medium',
'issue_time_cat_afternoon', 'issue_time_cat_early_hours',
'issue_time_cat_morning', 'issue_time_cat_night']

def Diff(li1, li2): 
    return (list(set(li1) - set(li2)))
    
current_vars = df_make_model.columns.tolist()

create_vars = Diff(vars_needed, current_vars)

for i in create_vars:
    df_make_model[i] = 0
    
# creating the model
import pickle as p

modelfile = 'final_prediction.pickle'
model = p.load(open(modelfile, 'rb'))

output = pd.DataFrame(model.predict_proba(df_make_model), columns=['not_top_25', 'top_25'])

output.to_csv(output_filepath, index=False)