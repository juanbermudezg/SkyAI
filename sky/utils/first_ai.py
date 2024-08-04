import pandas as pd
import joblib

model_filename='./sky/static/src/ai_models/FINAL.joblib'
def loadAirports():
    df = pd.read_csv('./sky/static/src/data/airports.csv')
    lista = df['Airport Code'].tolist()
    return lista
def prepare_input(year, month, day, hourSTD, minuteSTD, hourSTA, minuteSTA, airliner, from_location, to_location, all_airports):
    data = {
        'year': [year],
        'month': [month],
        'day': [day],
        'hourSTD': [hourSTD],
        'minuteSTD': [minuteSTD],
        'hourSTA': [hourSTA],
        'minuteSTA': [minuteSTA],
        'Airliner': [airliner]
    }
    input_df = pd.DataFrame(data)
    for airport in all_airports:
        input_df['FROM_' + airport] = from_location == airport
        input_df['TO_' + airport] = to_location == airport
    return input_df

def cargarModelo():
    loaded_model = joblib.load(model_filename)
    return loaded_model

