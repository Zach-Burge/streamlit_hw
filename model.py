import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pickle

df = pd.read_csv("/Users/burgefamily/CPSC325/dspl-pga-tour-project/data/ASA All PGA Raw Data - Tourn Level.csv")
df.drop(columns = ['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace = True)
# print(df['pos'])
df.replace('NA', np.nan, inplace=True)
# df['pos'] = df['pos'].fillna(999.0)
df.dropna(axis=0, inplace=True)
df.isna().any()

df = df[df['made_cut'] != 0]
df = df[df['n_rounds'] == 4]
df = df[df['strokes'] >= 250]

features = ['sg_putt', 'sg_arg', 'sg_app', 'sg_ott', 'sg_t2g', 'sg_total', 'player id']
target = ['strokes']

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

reg_rf = RandomForestRegressor(random_state=42)
reg_rf.fit(X_train, y_train)

# save
with open('model.pkl','wb') as f:
    pickle.dump(reg_rf,f)