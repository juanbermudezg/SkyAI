from datetime import date, time
from .first_ai import loadAirports, cargarModelo, prepare_input
from .sencond_ai import verificar_fecha_hora, new_Dataframe, make_prediction, adjust_time

def finalDef(dictFligth):
    allAirports = loadAirports()
    loaded_model_final = cargarModelo()
    expected_columns = loaded_model_final.feature_names_in_
    year = dictFligth.get('year')
    month = dictFligth.get('month')
    day = dictFligth.get('day')
    hourSTD = dictFligth.get('hourSTD')
    minuteSTD = dictFligth.get('minuteSTD')
    hourSTA = dictFligth.get('hourSTA')
    minuteSTA = dictFligth.get('minuteSTA')
    from_location = dictFligth.get('from_location')
    to_location = dictFligth.get('to_location')
    airliner = dictFligth.get('airliner')
    airlinerName = dictFligth.get('airlinerName')
    input_data = prepare_input(year, month, day, hourSTD, minuteSTD, hourSTA, minuteSTA, airliner, from_location, to_location, allAirports)
    for col in expected_columns:
        if col not in input_data:
            input_data[col] = False
    input_data = input_data[expected_columns]
    predictions = loaded_model_final.predict(input_data)
    status_text = predictions[0]
    airportsCompleted = ['BAQ', 'BOG', 'CLO', 'CTG', 'MDE', 'MIA', 'SMR']
    message = "Datos calculados exitosamente."
    if from_location in airportsCompleted and to_location in airportsCompleted:
        fecha_temp = date(year, month, day)
        hora_STD_temp = time(hourSTD, minuteSTD)
        hora_STA_temp = time(hourSTA, minuteSTA)
        resultados = verificar_fecha_hora(fecha_temp, hora_STD_temp, hora_STA_temp)
        new_data = new_Dataframe(airlinerName, from_location, to_location, year, month, day, hourSTD, minuteSTD, hourSTA, minuteSTA, resultados)
        predictions_second = make_prediction(new_data)
        hourATD, minuteATD = adjust_time(hourSTD, minuteSTD, predictions_second[0][0])
        hourATA, minuteATA = adjust_time(hourSTA, minuteSTA, predictions_second[0][1])
    else:
        hourATD = hourSTD  
        minuteATD = minuteSTD  
        hourATA = hourSTA  
        minuteATA = minuteSTA 
    
    return {
        'status_text': status_text,
        'hourATD': int(hourATD),
        'minuteATD': int(minuteATD),
        'hourATA': int(hourATA),
        'minuteATA': int(minuteATA),
        'message': message
    }

