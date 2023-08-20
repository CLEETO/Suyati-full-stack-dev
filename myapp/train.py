def train_model():
    from django.db import models
    from .models import modeldata

    listing=modeldata.objects.values(
        'livingAreaSqFt',
        'numOfBathrooms',
        'lotSizeSqFt',
        'numOfBedrooms',
        'numOfStories',
        'numOfPhotos',
        'hasSpa',
        'hasView',
        'numOfPatioAndPorchFeatures',
        'numOfParkingFeatures',
        'latest_saleyear',
        'numOfSecurityFeatures',
        'latestPrice')
    import pandas as pd
    housing_data = pd.DataFrame.from_records(listing)
    selected_features = list(housing_data.iloc[:, :-1])
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import StratifiedShuffleSplit, cross_val_score, cross_validate, GridSearchCV
    def standardize_dataframe(df, scaler=None):
        # Convert boolean columns to numerical (0 or 1); and standardize numerical columns
        bool_df = df[[col for col in df.columns if df.dtypes[col] == 'bool']].astype('float64')
        num_df = df[[col for col in df.columns if df.dtypes[col] == 'float64'
                    or df.dtypes[col] == 'int64']]
        # If scaler is given, use it. Otherwise train a new scaler on the numerical columns.
        if(scaler==None):
            scaler = StandardScaler().fit(num_df)
        num_df = pd.DataFrame(scaler.transform(num_df), columns=num_df.columns)
        
        # Ensure that bool_df has ascending indices just like num_df (since scaling resets indices)
        bool_df = bool_df.reset_index().drop(['index'], axis=1)
        
        return num_df.join(bool_df), scaler
    # Sampling hyperparameters
    test_size = 0.2
    intervals = [0, 250000, 400000, 600000, 800000, 1500000, housing_data['latestPrice'].max()]
    intervals.sort()
    price_categories = pd.cut(housing_data['latestPrice'], intervals)

    # Split into training and test sets
    split_func = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=46)
    indices = list(split_func.split(housing_data, price_categories))[0]
    training_data, test_data = housing_data.iloc[indices[0]], housing_data.iloc[indices[1]]
    x_train, y_train = training_data[selected_features], training_data['latestPrice']
    x_test, y_test = test_data[selected_features], test_data['latestPrice']
    y_train, y_test = y_train.reset_index()['latestPrice'], y_test.reset_index()['latestPrice']

    # Standardize the sets (using only parameters from training set)
    x_train, scaler = standardize_dataframe(x_train)
    x_test, _ = standardize_dataframe(x_test, scaler)
    # Full sets standardized
    x, y = pd.concat([x_train, x_test], ignore_index=True), pd.concat([y_train, y_test], ignore_index=True)
    #model_dir = 'C:/Users/CLEETO ITTIACHAN/suyati/realestate/myapp/SavedModels/'
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SavedModels')
    random_forest_regressor_name = "modelsrandom_forest_regressor"

    def save_sklearn_model(model, model_name):
        with open(model_dir + model_name + '.pkl', 'wb') as file:  pickle.dump(model, file)


    from sklearn.ensemble import RandomForestRegressor

    model = RandomForestRegressor()
    #best_params = {'n_estimators': 100, 'max_features': 4}
    #model = RandomForestRegressor(n_estimators=best_params['n_estimators'], max_features=best_params['max_features'])
    model = RandomForestRegressor(n_estimators=100, max_features=4)
    model.fit(x_train, y_train)
    save_sklearn_model(model, random_forest_regressor_name)
