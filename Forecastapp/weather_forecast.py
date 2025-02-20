import sqlite3
from datetime import datetime

import requests

from weather import Weather

API_KEY = "b91fc3cf5b981127900f92bdfb7b6a75"


class WeatherForecast:
    def __init__(self, db_path="forecast.db"):
        self.__db_path = db_path
        self.create_table_forecasts()

    def create_table_forecasts(self):
        with sqlite3.connect(self.__db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS forecasts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    country VARCHAR(100) NOT NULL,
                    city VARCHAR(100) NOT NULL,
                    temperature FLOAT NOT NULL,
                    description VARCHAR (150) NOT NULL,
                    wind_speed FLOAT NOT NULL,
                    date VARCHAR(100) NOT NULL
                )
                """
            )
            conn.commit()

    def save_forecast(self, forecast_list):

        formatted_forecast = [
            (
                forecast["city"],
                forecast["country"],
                float(forecast["temperature"]),
                forecast["description"],
                float(forecast["wind_speed"]),
                str(forecast["datetime"]),
            )
            for forecast in forecast_list
        ]
        with sqlite3.connect(self.__db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany(
                "INSERT INTO forecasts (city, country, temperature, description, wind_speed, date) VALUES (?,?,?,?,?,?)",
                formatted_forecast,
            )
        conn.commit()
        conn.close()

    def load_forecasts(self, city, start_date, end_date):
        with sqlite3.connect(self.__db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM forecasts WHERE city like ? AND date BETWEEN ? AND ? ORDER BY date",
                (city, start_date, end_date),
            )
            results = cursor.fetchall()
            return results

    def get_forencast(self, city, start_date, end_date):

        base_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&lang=pt_br&appid={API_KEY}&cnt=16"

        response = requests.get(base_url)

        if response.status_code != 200:
            raise RuntimeError(
                f"Erro ao obter previsão: {response.status_code} - {response.text}"
            )

        data = response.json()

        # Check for data returned
        if "list" not in data:
            raise ValueError(f"Nenhum dado de previsão disponível para '{city}'.")

        # Convert dates to datetime objects
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        # Filter forecasts by date range
        forecast_list = []
        for entry in data["list"]:
            forecast_date = datetime.fromtimestamp(entry["dt"])
            if start <= forecast_date <= end:
                forecast_list.append(
                    {
                        "city": data["city"]["name"],
                        "temperature": entry["main"]["temp"],
                        "description": entry["weather"][0]["description"],
                        "wind_speed": entry["wind"]["speed"],
                        "datetime": forecast_date.strftime("%Y-%m-%d"),
                        "country": data["city"]["country"],
                    }
                )
        self.save_forecast(forecast_list)
        return self.load_forecasts(city, start_date, end_date)
