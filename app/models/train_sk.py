from sklearn import linear_model
import pandas as pd
import numpy as np


df = pd.read_csv('../data/MINISTERIO DA EDUCACAO.csv', decimal=',', thousands='.')
data = df.loc[df['codigoNcmSh'] == 84433115]
X = data['quantidade']
y = data['valor']


reg = linear_model.Ridge(alpha=.5)
reg.fit(X.to_numpy().reshape(-1, 1), y.to_numpy().reshape(-1, 1))
# # print(predictor.params)

# # print(predictor.summary())

print(reg.predict(np.array([1,5,10]).reshape(-1,1)))

# predictor.save('')