from datetime import datetime, date, time
import holidays
import pandas as pd
import joblib

def adjust_time(hour, minute, adjustment_minutes):
    total_minutes = minute + adjustment_minutes
    additional_hours = total_minutes // 60
    final_minutes = total_minutes % 60
    if final_minutes < 0:
        final_minutes += 60
        additional_hours -= 1
    final_hour = (hour + additional_hours) % 24
    if final_hour < 0:
        final_hour += 24
    return final_hour, final_minutes

def make_prediction(new_data):
    loaded_model = joblib.load('./sky/static/src/ai_models/mejor_modelo_xgb.pkl')
    model_utils = {
        'load_model': lambda model_path: joblib.load(model_path),
        'load_scaler': lambda scaler_path: joblib.load(scaler_path),
        'scale_data': lambda scaler, data: scaler.transform(data),
        'predict': lambda model, data: model.predict(data)
    }
    model_path = './sky/static/src/ai_models/mejor_modelo_xgb.pkl'
    scaler_path = './sky/static/src/ai_models/scaler.pkl'
    model = model_utils['load_model'](model_path)
    scaler = model_utils['load_scaler'](scaler_path)
    new_data_scaled = model_utils['scale_data'](scaler, new_data)
    predictions = model_utils['predict'](model, new_data_scaled)
    return predictions

def es_fin_de_semana(fecha):
    return fecha.weekday() >= 5

def es_dia_festivo(fecha, pais='CO'):
    dias_festivos = holidays.country_holidays(pais)
    return fecha in dias_festivos

def es_hora_pico_el_dorado(hora):
    hora_inicio_mana = time(6, 0)
    hora_fin_mana = time(9, 0)
    hora_inicio_medio = time(11, 0)
    hora_fin_medio = time(14, 0)
    hora_inicio_tarde = time(17, 0)
    hora_fin_tarde = time(20, 0)
    
    return (
        (hora >= hora_inicio_mana and hora < hora_fin_mana) or
        (hora >= hora_inicio_medio and hora < hora_fin_medio) or
        (hora >= hora_inicio_tarde and hora < hora_fin_tarde)
    )

def es_vacaciones(fecha):
    year = fecha.year
    vacaciones_mitad = (date(year, 6, 15), date(year, 7, 15))
    vacaciones_fin = (date(year, 12, 15), date(year + 1, 1, 15))
    semana_santa = holidays.CO(years=[year]).get_named('Semana Santa')
    
    return (
        (vacaciones_mitad[0] <= fecha <= vacaciones_mitad[1]) or
        (vacaciones_fin[0] <= fecha <= vacaciones_fin[1]) or
        (fecha in semana_santa)
    )

def verificar_fecha_hora(fecha_hora, hora1, hora2, pais='CO'):
  
    
    return [
        es_fin_de_semana(fecha_hora),
        es_dia_festivo(fecha_hora, pais),
        es_vacaciones(fecha_hora),
        es_hora_pico_el_dorado(hora1),
        es_hora_pico_el_dorado(hora2)
        
    ]
def mapear_valores(airliner, from_code, to_code):
    airliner_mapping = {'Avianca': 0, 'Clic': 1, 'JetSMART': 2, 'LATAM Airlines': 3, 'Satena': 4}
    code_mapping = {'BAQ': 0, 'BOG': 1, 'CLO': 2, 'CTG': 3, 'MDE': 4, 'MIA': 5, 'SMR': 6}
    airliner_mapped = airliner_mapping.get(airliner, -1)
    from_code_mapped = code_mapping.get(from_code, -1)  
    to_code_mapped = code_mapping.get(to_code, -1)      
    return airliner_mapped, from_code_mapped, to_code_mapped

def new_Dataframe(airlinerName, from_location, to_location, year, month, day, hourSTD, minuteSTD, hourSTA, minuteSTA, resultados):
    airliner_mapped, from_code_mapped, to_code_mapped = mapear_valores(airlinerName, from_location, to_location)
    new_data = pd.DataFrame({
        'Airliner': [airliner_mapped],
        'FROM_CODE': [from_code_mapped],
        'TO_CODE': [to_code_mapped],
        'YEAR': [year],
        'MONTH': [month],
        'DAY': [day],
        'hourSTD': [hourSTD],
        'minuteSTD': [minuteSTD],
        'hourSTA': [hourSTA],
        'minuteSTA': [minuteSTA],
        'es_fin_de_semana': [resultados[0]],
        'es_dia_festivo': [resultados[1]],
        'es_vacaciones': [resultados[2]],
        'es_hora_pico_STD': [resultados[3]],
        'es_hora_pico_STA': [resultados[4]]
        })
    return new_data

