import pandas as pd
import numpy as np

import os

def clean_data():

    for subdir, dirs, files in os.walk(r'data/raw'):
        for filename in files:
            filepath = subdir + os.sep + filename
            data = pd.read_csv(filepath)

# Choose necessary colums
            data = data[["HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR", "HTHG", "HTAG", "HTR","HS","AS","HST","AST","HF","AF","HC","AC","HY","AY","HR","AR","B365H","B365D","B365A"]]
# Map Teams
            teams = data.HomeTeam.unique()
# Map Home Stats
            HS = []
            HC = []
            HF = []
            HY = []
            HR = []

            for i in range(len(teams)):
                home_shoots = 0
                home_corners = 0
                home_fouls = 0
                home_yellow = 0
                home_red = 0
                for j in range(len(data["HomeTeam"])):
                    if data["HomeTeam"][j] == teams[i]:
                        home_shoots += data["HS"][j]
                        home_corners += data["HC"][j]
                        home_fouls += data["HF"][j]
                        home_yellow += data["HY"][j]
                        home_red += data["HR"][j]
                    else:
                        continue

                HS.append(home_shoots)
                HC.append(home_corners)
                HF.append(home_fouls)
                HY.append(home_yellow)
                HR.append(home_red)

# Map Away Stats
            AS = []
            AC = []
            AF = []
            AY = []
            AR = []

            for i in range(len(teams)):
                away_shoots = 0
                away_corners = 0
                away_fouls = 0
                away_yellow = 0
                away_red = 0
                for j in range(len(data["AwayTeam"])):
                    if data["AwayTeam"][j] == teams[i]:
                        away_shoots += data["AS"][j]
                        away_corners += data["AC"][j]
                        away_fouls += data["AF"][j]
                        away_yellow += data["AY"][j]
                        away_red += data["AR"][j]
                    else:
                        continue

                AS.append(away_shoots)
                AC.append(away_corners)
                AF.append(away_fouls)
                AY.append(away_yellow)
                AR.append(away_red)

# Map Home Wins/Draws/Loss
            Home_Wins = []
            Home_Draws = []
            Home_Loss = []

            for i in range(len(teams)):
                home_wins = 0
                home_draws = 0
                home_loss = 0

                for j in range(len(data["AwayTeam"])):
                    if data["HomeTeam"][j] == teams[i] and data["FTR"][j] == "H":
                        home_wins += 1
                    elif data["HomeTeam"][j] == teams[i] and data["FTR"][j] == "D":
                        home_draws += 1
                    elif data["HomeTeam"][j] == teams[i] and data["FTR"][j] == "A":
                        home_loss += 1
                    else:
                        continue

                Home_Wins.append(home_wins)
                Home_Draws.append(home_draws)
                Home_Loss.append(home_loss)

# Map Away Wins/Draws/Loss
            Away_Wins = []
            Away_Draws = []
            Away_Loss = []

            for i in range(len(teams)):
                away_wins = 0
                away_draws = 0
                away_loss = 0

                for j in range(len(data["AwayTeam"])):
                    if data["AwayTeam"][j] == teams[i] and data["FTR"][j] == "A":
                        away_wins += 1
                    elif data["AwayTeam"][j] == teams[i] and data["FTR"][j] == "D":
                        away_draws += 1
                    elif data["AwayTeam"][j] == teams[i] and data["FTR"][j] == "H":
                        away_loss += 1
                    else:
                        continue

                Away_Wins.append(away_wins)
                Away_Draws.append(away_draws)
                Away_Loss.append(away_loss)

# Create Dictionaries for Stats and Teams

            HS_dictionary = dict(zip(teams, HS))
            AS_dictionary = dict(zip(teams, AS))
            HC_dictionary = dict(zip(teams, HC))
            AC_dictionary = dict(zip(teams, AC))
            HF_dictionary = dict(zip(teams, HF))
            AF_dictionary = dict(zip(teams, AF))
            HY_dictionary = dict(zip(teams, HY))
            AY_dictionary = dict(zip(teams, AY))
            HR_dictionary = dict(zip(teams, HR))
            AR_dictionary = dict(zip(teams, AR))
            HWin_dictionary = dict(zip(teams, Home_Wins))
            HDraw_dictionary = dict(zip(teams, Home_Draws))
            HLoss_dictionary = dict(zip(teams, Home_Loss))
            AWin_dictionary = dict(zip(teams, Away_Wins))
            ADraw_dictionary = dict(zip(teams, Away_Draws))
            ALoss_dictionary = dict(zip(teams, Away_Loss))

# Add Columns to Dataframe
            data['HomeShoot'] = data['HomeTeam'].map(HS_dictionary)
            data['HomeCorner'] = data['HomeTeam'].map(HC_dictionary)
            data['HomeFouls'] = data['HomeTeam'].map(HF_dictionary)
            data['HomeYellow'] = data['HomeTeam'].map(HY_dictionary)
            data['HomeRed'] = data['HomeTeam'].map(HR_dictionary)
            data['HomeWin'] = data['HomeTeam'].map(HWin_dictionary)
            data['HomeDraw'] = data['HomeTeam'].map(HDraw_dictionary)
            data['HomeLoss'] = data['HomeTeam'].map(HLoss_dictionary)

            data["AwayShoot"] = data['AwayTeam'].map(AS_dictionary)
            data["AwayCorner"] = data['AwayTeam'].map(AC_dictionary)
            data["AwayFouls"] = data['AwayTeam'].map(AF_dictionary)
            data["AwayYellow"] = data['AwayTeam'].map(AY_dictionary)
            data["AwayRed"] = data['AwayTeam'].map(AR_dictionary)
            data["AwayWin"] = data['AwayTeam'].map(AWin_dictionary)
            data["AwayDraw"] = data['AwayTeam'].map(ADraw_dictionary)
            data["AwayLoss"] = data['AwayTeam'].map(ALoss_dictionary)

# Choose necessary columns
            data = data[["HomeTeam", "AwayTeam", "FTR", "HomeShoot", "AwayShoot", "HomeCorner","AwayCorner","HomeFouls","AwayFouls","HomeYellow","AwayYellow","HomeRed","AwayRed","HomeWin","AwayWin","HomeDraw","AwayDraw","HomeLoss","AwayLoss", "B365H","B365D","B365A"]]
            data.to_csv(r'data/soccerdata_cleaned.csv', index = False)
# Export cleaned Dataframe to csv
            data.to_csv(r'data/clean/{}'.format(filename), index = False)

def dict_data(data):
# Import Data
    #data = pd.read_csv(data_string)
# Choose necessary colums
    data = data[["HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR", "HTHG", "HTAG", "HTR","HS","AS","HST","AST","HF","AF","HC","AC","HY","AY","HR","AR","B365H","B365D","B365A"]]
# Map Teams
    teams = data.HomeTeam.unique()
# Map Home Stats
    HS = []
    HC = []
    HF = []
    HY = []
    HR = []

    for i in range(len(teams)):
        home_shoots = 0
        home_corners = 0
        home_fouls = 0
        home_yellow = 0
        home_red = 0
        for j in range(len(data["HomeTeam"])):
            if data["HomeTeam"][j] == teams[i]:
                home_shoots += data["HS"][j]
                home_corners += data["HC"][j]
                home_fouls += data["HF"][j]
                home_yellow += data["HY"][j]
                home_red += data["HR"][j]
            else:
                continue

        HS.append(home_shoots)
        HC.append(home_corners)
        HF.append(home_fouls)
        HY.append(home_yellow)
        HR.append(home_red)

# Map Away Stats
    AS = []
    AC = []
    AF = []
    AY = []
    AR = []

    for i in range(len(teams)):
        away_shoots = 0
        away_corners = 0
        away_fouls = 0
        away_yellow = 0
        away_red = 0
        for j in range(len(data["AwayTeam"])):
            if data["AwayTeam"][j] == teams[i]:
                away_shoots += data["AS"][j]
                away_corners += data["AC"][j]
                away_fouls += data["AF"][j]
                away_yellow += data["AY"][j]
                away_red += data["AR"][j]
            else:
                continue

        AS.append(away_shoots)
        AC.append(away_corners)
        AF.append(away_fouls)
        AY.append(away_yellow)
        AR.append(away_red)

# Map Home Wins/Draws/Loss
    Home_Wins = []
    Home_Draws = []
    Home_Loss = []

    for i in range(len(teams)):
        home_wins = 0
        home_draws = 0
        home_loss = 0

        for j in range(len(data["AwayTeam"])):
            if data["HomeTeam"][j] == teams[i] and data["FTR"][j] == "H":
                home_wins += 1
            elif data["HomeTeam"][j] == teams[i] and data["FTR"][j] == "D":
                home_draws += 1
            elif data["HomeTeam"][j] == teams[i] and data["FTR"][j] == "A":
                home_loss += 1
            else:
                continue

        Home_Wins.append(home_wins)
        Home_Draws.append(home_draws)
        Home_Loss.append(home_loss)

# Map Away Wins/Draws/Loss
    Away_Wins = []
    Away_Draws = []
    Away_Loss = []

    for i in range(len(teams)):
        away_wins = 0
        away_draws = 0
        away_loss = 0

        for j in range(len(data["AwayTeam"])):
            if data["AwayTeam"][j] == teams[i] and data["FTR"][j] == "A":
                away_wins += 1
            elif data["AwayTeam"][j] == teams[i] and data["FTR"][j] == "D":
                away_draws += 1
            elif data["AwayTeam"][j] == teams[i] and data["FTR"][j] == "H":
                away_loss += 1
            else:
                continue

        Away_Wins.append(away_wins)
        Away_Draws.append(away_draws)
        Away_Loss.append(away_loss)

# Create Dictionaries for Stats and Teams

    HS_dictionary = dict(zip(teams, HS))
    AS_dictionary = dict(zip(teams, AS))
    HC_dictionary = dict(zip(teams, HC))
    AC_dictionary = dict(zip(teams, AC))
    HF_dictionary = dict(zip(teams, HF))
    AF_dictionary = dict(zip(teams, AF))
    HY_dictionary = dict(zip(teams, HY))
    AY_dictionary = dict(zip(teams, AY))
    HR_dictionary = dict(zip(teams, HR))
    AR_dictionary = dict(zip(teams, AR))
    HWin_dictionary = dict(zip(teams, Home_Wins))
    HDraw_dictionary = dict(zip(teams, Home_Draws))
    HLoss_dictionary = dict(zip(teams, Home_Loss))
    AWin_dictionary = dict(zip(teams, Away_Wins))
    ADraw_dictionary = dict(zip(teams, Away_Draws))
    ALoss_dictionary = dict(zip(teams, Away_Loss))

# Add Columns to Dataframe
    data['HomeShoot'] = data['HomeTeam'].map(HS_dictionary)
    data['HomeCorner'] = data['HomeTeam'].map(HC_dictionary)
    data['HomeFouls'] = data['HomeTeam'].map(HF_dictionary)
    data['HomeYellow'] = data['HomeTeam'].map(HY_dictionary)
    data['HomeRed'] = data['HomeTeam'].map(HR_dictionary)
    data['HomeWin'] = data['HomeTeam'].map(HWin_dictionary)
    data['HomeDraw'] = data['HomeTeam'].map(HDraw_dictionary)
    data['HomeLoss'] = data['HomeTeam'].map(HLoss_dictionary)

    data["AwayShoot"] = data['AwayTeam'].map(AS_dictionary)
    data["AwayCorner"] = data['AwayTeam'].map(AC_dictionary)
    data["AwayFouls"] = data['AwayTeam'].map(AF_dictionary)
    data["AwayYellow"] = data['AwayTeam'].map(AY_dictionary)
    data["AwayRed"] = data['AwayTeam'].map(AR_dictionary)
    data["AwayWin"] = data['AwayTeam'].map(AWin_dictionary)
    data["AwayDraw"] = data['AwayTeam'].map(ADraw_dictionary)
    data["AwayLoss"] = data['AwayTeam'].map(ALoss_dictionary)


    home_dicts = [HS_dictionary, HC_dictionary, HF_dictionary, HY_dictionary, HR_dictionary, HWin_dictionary, HDraw_dictionary, HLoss_dictionary]

    d_home = {}
    for k in HS_dictionary.keys():
        d_home[k] = tuple(home_dict[k] for home_dict in home_dicts)

    away_dicts = [AS_dictionary, AC_dictionary, AF_dictionary, AY_dictionary, AR_dictionary, AWin_dictionary, ADraw_dictionary, ALoss_dictionary]

    d_away = {}
    for k in AS_dictionary.keys():
        d_away[k] = tuple(away_dict[k] for away_dict in away_dicts)
# Choose necessary columns
    
    return d_home, d_away
# Export cleaned Dataframe to csv
#data.to_csv(r'data/soccerdata_cleaned.csv', index = False)
