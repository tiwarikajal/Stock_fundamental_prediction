###TESTING LINEAR MODEL FIRST

import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression,Ridge
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.tree import DecisionTreeRegressor

final_df=pd.read_pickle('Final_dataset_structured.pkl')

x= final_df['x']
y = final_df['y']
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2,shuffle=False)
y_train, y_test = y_train.astype(float), y_test.astype(float)

#Using Linear
reg = LinearRegression().fit(np.stack(X_train),np.stack(y_train))
reg.fit(np.stack(X_train),np.stack(y_train))
y_pred=reg.predict(np.stack(X_test))
print("MSE with linear regression:",mean_squared_error(y_pred,y_test))
print("R2 Score",r2_score(y_test, y_pred))

##Using Decision Tree
reg = DecisionTreeRegressor().fit(np.stack(X_train),np.stack(y_train))
y_pred=reg.predict(np.stack(X_test))
print("MSE with Decision Tree regression:",mean_squared_error(y_pred,y_test))
print("R2 Score with Decision Tree regression",r2_score(y_test, y_pred))


##Using Regularization with ridge
reg = Ridge(alpha=1)
reg.fit(np.stack(X_train),np.stack(y_train))
y_pred=reg.predict(np.stack(X_test))
print("MSE with Ridge regression:",mean_squared_error(y_pred,y_test))
print("R2 Score with Ridge regression",r2_score(y_test, y_pred))
print(reg.coef_)