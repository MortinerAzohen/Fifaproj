# Machine Learning Algorithms
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from Data_operations.Prepare_data import DataOperations
# Model Selection and Evaluation
from sklearn.model_selection import train_test_split, KFold, cross_validate
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import seaborn as sb
# Performance
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

def display_scores(scores):
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation:", scores.std())


fifa_data = DataOperations()
fifa_dataset = fifa_data.import_data()


X = fifa_dataset.drop('Price', axis = 1)
y = fifa_dataset['Price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)


# regresja liniowa
print("\n regresja liniowa test/train set")
lin_reg = LinearRegression(normalize=True, n_jobs=-1)
lin_reg.fit(X_train, y_train)
y_pred = lin_reg.predict(X_test)
print('Mean squared error: %.2f'
      % np.sqrt(mean_squared_error(y_test, y_pred)))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_score(y_test, y_pred))
#drzwko decyzyjne
print("\n drzewko decyzyjne test/train set")
tree_reg = DecisionTreeRegressor(random_state=42)
tree_reg.fit(X_train, y_train)
y_pred = tree_reg.predict(X_test)

print('Mean squared error: %.2f'
      % np.sqrt(mean_squared_error(y_test, y_pred)))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_score(y_test, y_pred))
#random forest
print("\n random forest test/train set")
forest_reg = RandomForestRegressor(n_estimators=100, random_state=42)
forest_reg.fit(X_train, y_train)

y_pred = forest_reg.predict(X_test)
print('Mean squared error: %.2f'
      % np.sqrt(mean_squared_error(y_test, y_pred)))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_score(y_test, y_pred))
#extra trees reg
print("\n extra trees reg test/train set")
extra_reg = ExtraTreesRegressor(n_estimators=100, random_state=0)
extra_reg.fit(X_train, y_train)
y_pred = extra_reg.predict(X_test)

print('Mean squared error: %.2f'
      % np.sqrt(mean_squared_error(y_test, y_pred)))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_score(y_test, y_pred))

#gradient boost regressor
print("\n gradient boost regresor test/train set")
grad_reg = GradientBoostingRegressor(random_state=0)
grad_reg.fit(X_train,y_train)
y_pred = grad_reg.predict(X_test)

print('Mean squared error: %.2f'
      % np.sqrt(mean_squared_error(y_test, y_pred)))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_score(y_test, y_pred))

print("\n drzewko decyzyjne cross validation")
#cross-validation

scores = cross_validate(tree_reg, X, y,scoring=('r2','neg_mean_squared_error'), cv=KFold(n_splits = 10, shuffle = True, random_state = 42))
print("R2_score :",scores["test_r2"].mean())
tree_rmse_scores = np.sqrt(-scores["test_neg_mean_squared_error"])
display_scores(tree_rmse_scores)
print("\nregresja liniowa cross validation")
scores = cross_validate(lin_reg, X, y,scoring=('r2','neg_mean_squared_error'), cv=KFold(n_splits = 10, shuffle = True, random_state = 42))
print("R2_score:",scores["test_r2"].mean())
lin_rmse_scores = np.sqrt(-scores["test_neg_mean_squared_error"])
display_scores(lin_rmse_scores)
print("\nforest regression cross validation")
scores = cross_validate(forest_reg, X, y,scoring=('r2','neg_mean_squared_error'), cv=KFold(n_splits = 10, shuffle = True, random_state = 42))
print("R2_score:",scores["test_r2"].mean())
forest_rmse_scores = np.sqrt(-scores["test_neg_mean_squared_error"])
display_scores(forest_rmse_scores)
print("\ngradient regresion cross validation")
scores = cross_validate(grad_reg, X, y,scoring=('r2','neg_mean_squared_error'), cv=KFold(n_splits = 10, shuffle = True, random_state = 42))
print("R2_score:",scores["test_r2"].mean())
grad_rmse_scores = np.sqrt(-scores["test_neg_mean_squared_error"])
display_scores(grad_rmse_scores)
print("\nextra trees regresion cross validation")
scores = cross_validate(extra_reg, X, y,scoring=('r2','neg_mean_squared_error'), cv=KFold(n_splits = 10, shuffle = True, random_state = 42))
print("R2_score:",scores["test_r2"].mean())
extra_rmse_scores = np.sqrt(-scores["test_neg_mean_squared_error"])
display_scores(extra_rmse_scores)

param_grid = [
    {'n_estimators': [3, 10, 30], 'max_features': [2, 3, 4]},
    {'bootstrap': [False], 'n_estimators': [3, 10], 'max_features': [2, 3, 4]},
  ]
#grid_search - forest_reg
grid_search = GridSearchCV(forest_reg, param_grid, cv=5,
                           scoring='neg_mean_squared_error',
                           return_train_score=True)

grid_search.fit(X_train, y_train)

print(grid_search.best_params_)

final_model = grid_search.best_estimator_

final_predictions = final_model.predict(X_test)

print('Mean squared error: %.2f'
      % np.sqrt(mean_squared_error(y_test, final_predictions)))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_score(y_test, final_predictions))
#grid search extratrees regressor
grid_search = GridSearchCV(extra_reg, param_grid, cv=5,
                           scoring='neg_mean_squared_error',
                           return_train_score=True)

grid_search.fit(X_train, y_train)

print(grid_search.best_params_)

final_model = grid_search.best_estimator_

final_predictions = final_model.predict(X_test)

print('Mean squared error: %.2f'
      % np.sqrt(mean_squared_error(y_test, final_predictions)))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_score(y_test, final_predictions))

#grid search gradient regressor
param_grid = {
    'loss': ['ls','lad'],
    'learning_rate': [0.1,0.5,0.9],
    'criterion': ['mse'],
    'min_samples_leaf': [1,2,3],
    'min_samples_split': [2, 4,6],
    'n_estimators': [100, 200]
}
grid_search = GridSearchCV(grad_reg, param_grid, cv = 3,scoring='neg_mean_squared_error',
                           return_train_score=True)

grid_search.fit(X_train, y_train)

print(grid_search.best_params_)

final_model = grid_search.best_estimator_

final_predictions = final_model.predict(X_test)

print('Mean squared error: %.2f'
      % np.sqrt(mean_squared_error(y_test, final_predictions)))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_score(y_test, final_predictions))
