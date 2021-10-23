from numpy.lib.function_base import copy
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, RobustScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import FeatureUnion

def preprocess_data(dataframe):
# import data
    #data = pd.read_csv("data/soccerdata_cleaned.csv")
    data = dataframe.copy()
# encode Output Variable
    data["FTR"] = data["FTR"].replace("H", 1)
    data["FTR"] = data["FTR"].replace("D", 2)
    data["FTR"] = data["FTR"].replace("A", 3)

# Train Test Split
    input_features = [
    'HomeShoot', 'HomeCorner', 'HomeFouls', 
    'HomeYellow', 'HomeRed', 'HomeWin', 
    'HomeDraw', 'HomeLoss', 'AwayShoot', 
    'AwayCorner', 'AwayFouls', 'AwayYellow',
    'AwayRed', 'AwayWin', 'AwayDraw',
    'AwayLoss',
    ]

    output_features = [
    "FTR" 
    ]

    X_train, X_test, y_train, y_test = train_test_split(
    data[input_features],
    data[output_features],
    random_state = 42
    )

    return X_train, X_test, y_train, y_test