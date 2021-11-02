from typing import Text
import streamlit as st
import pandas as pd
import joblib
import numpy as np
# Logistic Regression Model
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

from cleaning import *
from preprocessing import *

# title
st.title("ML Soccer Predictor")

game_day = st.number_input('GameDay', min_value=1, max_value=34, value=10, step=1)

if st.button("Download"):
    Season_2021 = pd.read_csv(r"https://www.football-data.co.uk/mmz4281/2122/D1.csv")
    Season_2020 = pd.read_csv(r"https://www.football-data.co.uk/mmz4281/2021/D1.csv")
    #Season_2020_c = pd.concat(Season_2020, axis=0, ignore_index=True)
    Season_2019 = pd.read_csv(r"https://www.football-data.co.uk/mmz4281/1920/D1.csv")
    Season_2018 = pd.read_csv(r"https://www.football-data.co.uk/mmz4281/1819/D1.csv")
    Season_2017 = pd.read_csv(r"https://www.football-data.co.uk/mmz4281/1718/D1.csv")
    Season_2016 = pd.read_csv(r"https://www.football-data.co.uk/mmz4281/1617/D1.csv")
    Season_2015 = pd.read_csv(r"https://www.football-data.co.uk/mmz4281/1516/D1.csv")
    Season_2014 = pd.read_csv(r"https://www.football-data.co.uk/mmz4281/1415/D1.csv")
    Season_2013 = pd.read_csv(r"https://www.football-data.co.uk/mmz4281/1314/D1.csv")
    Season_2012 = pd.read_csv(r"https://www.football-data.co.uk/mmz4281/1213/D1.csv")

    Season_list = [
               Season_2021,
               Season_2020,
               Season_2019,
               Season_2018,
               Season_2017,
               Season_2016,
               Season_2015,
               Season_2014,
               Season_2013,
               Season_2012,
               ]
    Seasons = ["Season_2021", "Season_2020", "Season_2019", "Season_2018", "Season_2017", "Season_2016", "Season_2015", "Season_2014", "Season_2013", "Season_2012"]
    db_concat = pd.concat(Season_list)
    for i in range(len(Season_list)):
        Season_list[i][0:(game_day * 9)].to_csv(r'data/raw/data_{}.csv'.format(Seasons[i]), index=False)
    db_concat.to_csv(r"data/data.csv")
    st.success("Download successful")

if st.button("Display Data"):
    data = pd.read_csv("data/data.csv")
    st.dataframe(data)

if st.button("Clean Data"):
    #data = pd.read_csv("data/data.csv")
    #data = clean_data(data)
    clean_data()
    #data.to_csv(r'data/data_clean.csv', index=False)
    #st.dataframe()
    st.success("Cleaning successful")

if st.button("Merge Historical Data"):
    df_2017 = pd.read_csv("data/clean/data_Season_2017.csv")
    df_2018 = pd.read_csv("data/clean/data_Season_2018.csv")
    df_2019 = pd.read_csv("data/clean/data_Season_2019.csv")
    df_2020 = pd.read_csv("data/clean/data_Season_2020.csv")
    df_2021 = pd.read_csv("data/clean/data_Season_2021.csv")
    result = df_2017.append([df_2018, df_2019, df_2020, df_2021])
    result.to_csv(r'data/data_clean.csv', index=False)

    st.success("Merging successful")
    

if st.button("Preprocess Data"):
    data = pd.read_csv("data/data_clean.csv")
    X_train, X_test, y_train, y_test = preprocess_data(data)
    st.success("Data successful preprocessesd")

filename = 'finalized_model.sav'

model = st.selectbox(
    'Choose Model',
    ('Logistic Regression', 'Naive Bayes Classifier', 'Decision Tree'))

if st.button("Train Model"):
    if model == "Logistic Regression":
        logistic_model = LogisticRegression()
        data = pd.read_csv("data/data_clean.csv")
        X_train, X_test, y_train, y_test = preprocess_data(data)
        logistic_model.fit(X_train, y_train)
        logistic_prediction = logistic_model.predict(X_test)
        test_score_log = round(logistic_model.score(X_test, y_test),2)
    # save the model to disk
        joblib.dump(logistic_model, filename)

        st.text("The Logistic Regression model achieves an accuracy from: {}".format(test_score_log))

    elif model == "Naive Bayes Classifier":
        nb_model = GaussianNB()
        data = pd.read_csv("data/data_clean.csv")
        X_train, X_test, y_train, y_test = preprocess_data(data)
        nb_model.fit(X_train, y_train)
        nb_prediction = nb_model.predict(X_test)
        test_score_nb = round(nb_model.score(X_test, y_test),2)
    # save the model to disk
        joblib.dump(nb_model, filename)

        st.text("The Naive Bayes model achieves an accuracy from: {}".format(test_score_nb))

    elif model == "Decision Tree":
        dt_model = DecisionTreeClassifier()
        data = pd.read_csv("data/data_clean.csv")
        X_train, X_test, y_train, y_test = preprocess_data(data)
        dt_model.fit(X_train, y_train)
        dt_prediction = dt_model.predict(X_test)
        test_score_dt = round(dt_model.score(X_test, y_test),2)
    # save the model to disk
        joblib.dump(dt_model, filename)

        st.text("The Decision Tree model achieves an accuracy from: {}".format(test_score_dt))

    

data = pd.read_csv("data/raw/data_Season_2021.csv")

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
    st.text("Home Shoots: {}".format(home_dict[hometeam][0]))
    st.text("Home Corners: {}".format(home_dict[hometeam][1]))
    st.text("Home Fouls: {}".format(home_dict[hometeam][2]))
    st.text("Yellow Cards: {}".format(home_dict[hometeam][3]))
    st.text("Red Cards: {}".format(home_dict[hometeam][4]))
    st.text("Home Wins: {}".format(home_dict[hometeam][5]))
    st.text("Home Draws: {}".format(home_dict[hometeam][6]))
    st.text("Home Loss: {}".format(home_dict[hometeam][7]))
    #st.text(home_team_data)

if st.button("Get Away Team Data"):

    away_team_data = away_dict[hometeam]
    st.subheader(awayteam)
    st.text("Away Shoots: {}".format(away_dict[awayteam][0]))
    st.text("Away Corners: {}".format(away_dict[awayteam][1]))
    st.text("Away Fouls: {}".format(away_dict[awayteam][2]))
    st.text("Yellow Cards: {}".format(away_dict[awayteam][3]))
    st.text("Red Cards: {}".format(away_dict[awayteam][4]))
    st.text("Away Wins: {}".format(away_dict[awayteam][5]))
    st.text("Away Draws: {}".format(away_dict[awayteam][6]))
    st.text("Away Loss: {}".format(away_dict[awayteam][7]))
    #st.text(away_team_data)

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


















