import pandas as pd
import pickle

def day_predict(lst):
    season = ['1', '2', '3', '4']
    mnth = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    holiday = ['0', '1']
    weekday = ['0', '1', '2', '3', '4', '5', '6']
    workingday = ['0', '1']
    weathersit = ['1', '2', '3']

    season = pd.DataFrame(season)
    mnth = pd.DataFrame(mnth)
    holiday = pd.DataFrame(holiday)
    weekday = pd.DataFrame(weekday)
    workingday = pd.DataFrame(workingday)
    weathersit = pd.DataFrame(weathersit)

    data = pd.concat([season, mnth, holiday, weekday, workingday, weathersit], axis=1)
    data.columns = ['season', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']

    categorical_cols = ['season', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']
    data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

    dat = data.head(1)

    for col in dat.columns:
        dat[col].values[:] = 0

    new_number = lst
    # new_number = [temp, hum, windspeed, season, mnth, holiday, weekday,workingday, weathersit]
    data_new = pd.DataFrame(new_number)
    print(data_new)
    # data_new=data_new.T
    data_new.columns = ['season', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'hum', 'windspeed']

    data_new.columns = [f"season_{data_new['season'][0]}", f"mnth_{data_new['mnth'][0]}",
                        f"holiday_{data_new['holiday'][0]}", f"weekday_{data_new['weekday'][0]}",
                        f"workingday_{data_new['workingday'][0]}", f"weathersit_{data_new['weathersit'][0]}", 'temp',
                        'hum', 'windspeed']

    cat = data_new.iloc[:, 0:6]
    num = data_new.iloc[:, 6:]

    lis1=['season_1', 'mnth_1', 'holiday_0', 'weekday_0', 'workingday_0', 'weathersit_1']

    lis=[]
    for i in cat.columns:
        if i in lis1:
            lis.append(i)

    cat = cat.drop(columns=lis, axis=1)

    for col in cat.columns:
        dat[col].values[:]=1

    new = pd.concat([num, dat], axis=1)

    file = open("D:\Work\Rental Bike Share Prediction\Rental Bike Share Prediction\predictions\dayfinalmodel.sav", 'rb')
    model = pickle.load(file)

    result = model.predict(new)
    return result


