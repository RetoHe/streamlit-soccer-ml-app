from typing import Text
import streamlit as st
import pandas as pd
import joblib
import numpy as np
# Logistic Regression Model
from sklearn.linear_model import LogisticRegression

from cleaning import *
from preprocessing import *

# title
st.title("ML Soccer Predictor")

if st.button("Download"):
    Season_2021 = pd.read_csv(r"https://www.football-data.co.uk/mmz4281/2122/D1.csv")
    #Season_2020_c = pd.concat(Season_2020, axis=0, ignore_index=True)
    #Season_2019 = pd.read_csv(r"https://www.football-data.co.uk/mmz4281/1920/D1.csv")

    Season_list = [
               Season_2021,
               ]
    db_concat = pd.concat(Season_list)
    db_concat.to_csv(r'data/data.csv', index=False)
    st.success("Download successful")

if st.button("Display Data"):
    data = pd.read_csv("data/data.csv")
    st.dataframe(data)

if st.button("Clean Data"):
    data = pd.read_csv("data/data.csv")
    data = clean_data(data)
    data.to_csv(r'data/data_clean.csv', index=False)
    st.dataframe(data)
    

if st.button("Preprocess Data"):
    data = pd.read_csv("data/data_clean.csv")
    X_train, X_test, y_train, y_test = preprocess_data(data)
    st.success("Data successful preprocessesd")

filename = 'finalized_model.sav'

if st.button("Train Model"):
    logistic_model = LogisticRegression()
    data = pd.read_csv("data/data_clean.csv")
    X_train, X_test, y_train, y_test = preprocess_data(data)
    logistic_model.fit(X_train, y_train)
    logistic_prediction = logistic_model.predict(X_test)
    test_score_log = round(logistic_model.score(X_test, y_test),2)
    # save the model to disk
    joblib.dump(logistic_model, filename)

    st.text("The model achieves an accuracy from: {}".format(test_score_log))

data = pd.read_csv("data/data.csv")

teams = data["HomeTeam"].unique()

hometeam = st.selectbox(
    'Choose HomeTeam',
    teams)

awayteam = st.selectbox(
    'Choose AwayTeam',
    teams)

home_dict, away_dict = dict_data(data)

if st.button("Get Home Team Data"):

    home_team_data = home_dict[hometeam]
    st.subheader(hometeam)
    st.text(home_team_data)

if st.button("Get Away Team Data"):

    away_team_data = away_dict[hometeam]
    st.subheader(awayteam)
    st.text(away_team_data)

result_dict = {1: "HomeWin", 2: "Draw", 3: "AwayWin"}

if st.button("Predict"):
    X_test = []
    for value in home_dict[hometeam]:
        X_test.append(value)

    for value in away_dict[awayteam]:
        X_test.append(value)
    # load the model from disk
    loaded_model = joblib.load(filename)
    result = loaded_model.predict([X_test])
    st.success(result_dict[int(result)])

if st.button("Get Probabilities"):
    X_test = []
    for value in home_dict[hometeam]:
        X_test.append(value)

    for value in away_dict[awayteam]:
        X_test.append(value)
    # load the model from disk
    loaded_model = joblib.load(filename)
    probabilities = loaded_model.predict_proba([X_test])
    st.text("Probability Home Win {} %".format(round(probabilities[0][0]*100),2))
    st.text("Probability Draw {} %".format(round(probabilities[0][1]*100),2))
    st.text("Probability Away Win {} %".format(round(probabilities[0][2]*100),2))


















