from cat.mad_hatter.decorators import tool
import requests
import geocoder
import pytz
import datetime

def map(weathercode):
    mappa_meteo = {
        0: "Cielo sereno",
        1: "Molto sereno",
        2: "Parzialmente nuvoloso",
        3: "Coperto",
        45: "Nebbia",
        48: "Nebbia con deposito di rima",
        51: "Pioviggine: Leggera intensità",
        53: "Pioviggine: Moderata intensità",
        55: "Pioviggine: Intensa intensità",
        56: "Pioviggine ghiacciata: Leggera intensità",
        57: "Pioviggine ghiacciata: Intensa intensità",
        61: "Pioggia: Leggera intensità",
        63: "Pioggia: Moderata intensità",
        65: "Pioggia: Forte intensità",
        66: "Pioggia ghiacciata: Leggera intensità",
        67: "Pioggia ghiacciata: Forte intensità",
        71: "Neve: Leggera intensità",
        73: "Neve: Moderata intensità",
        75: "Neve: Forte intensità",
        77: "Granulo di neve",
        80: "Piogge: Leggera intensità",
        81: "Piogge: Moderata intensità",
        82: "Piogge: Violenta intensità",
        85: "Rovesci di neve leggeri",
        86: "Rovesci di neve intensi",
        95: "Temporale: Debole intensità",
        96: "Temporale con grandine: Debole intensità",
        99: "Temporale con grandine: Forte intensità"
    }

    return mappa_meteo.get(weathercode, "Descrizione non disponibile")

def get_current_weather_code(data):
    tz = pytz.timezone('Europe/Rome')
    current_time = datetime.datetime.now(tz).isoformat()  # Ottieni l'ora corrente nel formato ISO8601
    
    # Cerca l'intervallo orario in cui rientra l'ora corrente
    time_array = data["hourly"]["time"]
    for i in range(len(time_array) - 1):
        start_time = time_array[i]
        end_time = time_array[i + 1]
        if start_time <= current_time < end_time:
            weather_code = data["hourly"]["weathercode"][i]
            return weather_code
    
    # Se l'ora corrente non è compresa in nessun intervallo, restituisci None
    return None
    
def get_weather_forecast(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=weathercode&timezone=Europe%2FLondon&forecast_days=1"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
            print("Risposta JSON:")
            print(weather_data)
            current_weather_code = get_current_weather_code(weather_data)
            if current_weather_code is not None:
                return map(current_weather_code)
            else:
                return "Nessun dato meteo disponibile per l'ora corrente."
        else:
            return "Errore"
    except Exception as e:
        return "Errore"

@tool()   
def get_weather(query, cat):
    """
    When user asks you to "che tempo fa" always use this tool.
    
    """
    location = geocoder.ip('me')
    print(location)
    # Verifica se la richiesta ha avuto successo
    if location.status == 'OK':
        latitude = location.latlng[0]
        longitude = location.latlng[1]
        print(f"Latitudine: {latitude}")
        print(f"Longitudine: {longitude}")
        return get_weather_forecast(latitude, longitude)
    else:
        return "Non riesco a capire dove ci troviamo"

