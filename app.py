from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    error = None

    if request.method == "POST":
        name = request.form.get("city", "").strip()
        if not name:
            error = "Please enter a city name!"
        else:
            weather_url = f"https://wttr.in/{name}?format=j1"
            response = requests.get(weather_url)

            if response.status_code == 200:
                weather = response.json()
                current = weather["current_condition"][0]
                lat = weather["nearest_area"][0]["latitude"]
                lon = weather["nearest_area"][0]["longitude"]

                time_api = f"http://api.timezonedb.com/v2.1/get-time-zone?key=IU1PHENQP1W5&format=json&by=position&lat={lat}&lng={lon}"
                time_response = requests.get(time_api)

                if time_response.status_code == 200:
                    timedata = time_response.json()
                    localtime = timedata.get("formatted", "Unavailable")
                else:
                    localtime = "Unavailable"

                weather_data = {
                    "city": name.title(),
                    "desc": current["weatherDesc"][0]["value"],
                    "temp": current["temp_C"],
                    "humidity": current["humidity"],
                    "wind": current["windspeedKmph"],
                    "time": localtime
                }
            else:
                error = "❌ Couldn't fetch weather data."

    return render_template("index.html", weather=weather_data, error=error)
if __name__ == "__main__":
    app.run(debug=True)