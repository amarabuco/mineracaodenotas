import statsmodels.api as sm
import pandas as pd

df = pd.read_csv('../data/MINISTERIO DA EDUCACAO.csv', decimal=',', thousands='.')
data = df.loc[df['codigoNcmSh'] == 84433115]
X = data['quantidade']
y = data['valor']

print(X)

model = sm.regression.linear_model.OLS(y, X)
predictor = model.fit()
# print(predictor.params)

# print(predictor.summary())

print(predictor.predict(1))
print(predictor.predict(5))
print(predictor.predict(10))

# predictor.save('')