import requests
from twilio.rest import Client
from tkinter import *
import os

API_KEY = os.environ.get("API_KEY")
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

BLUE = "#A1CDF1"
FONT_NAME = "Roboto"

parameters = {
    "lat" : 51.401720,
    "lon" : -0.150530,
    "appid" : API_KEY,
    "cnt" : 4
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()

weather_data = response.json()
day_1 = weather_data["list"][0]["weather"][0]["id"]
day_2 = weather_data["list"][1]["weather"][0]["id"]
day_3 = weather_data["list"][2]["weather"][0]["id"]
day_4 = weather_data["list"][3]["weather"][0]["id"]


day = 0
will_rain = False
will_snow = False
will_thunderstorm = False

while day < 1:
    weather_id = weather_data["list"][day]["weather"][0]["id"]
    print(weather_id)
    day += 1
    if 200 <= weather_id <= 232:
        will_thunderstorm = True

    if 500 <= weather_id <= 531:
        will_rain = True

    if 600 <= weather_id <= 622:
        will_snow = True

    if weather_id > 622:
        print("No extreme weather conditions tomorrow.")

def send_message():
    uk_number = f"+44{text_box.get("1.0", END)}"

    if will_rain:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages \
            .create(
            body="It's going to rain today, bring an umbrella 🌧️",
            from_="+12542523161",
            to=uk_number
        )
        print(message.status)

    if will_snow:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages \
            .create(
            body="It's going to snow today, get ready to build a snowman ⛄",
            from_="+12542523161",
            to=uk_number
        )
        print(message.status)

    if will_thunderstorm:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages \
            .create(
            body="There's going to be a thunderstorm today, be careful 🌩️",
            from_="+12542523161",
            to=uk_number
        )
        print(message.status)



window = Tk()
window.title("Weather Application")
window.config(bg=BLUE)

canvas = Canvas(width=512, height=512, bg=BLUE, highlightthickness=0)
cloud_img = PhotoImage(file="669958_weather_cloud_forecast_sun_icon.png")
canvas.create_image(256, 256, image=cloud_img)
canvas.grid(row=0, column=1)

text_label = Label()
text_label.config(text="Enter phone number:", bg=BLUE, font=(FONT_NAME, 16 , "bold"))
text_label.grid(row=1, column=1)

text_box = Text(height=1, width=20)
text_box.grid(row=2, column=1)

submit_button = Button(command=send_message, text="Submit", font=(FONT_NAME, 8 , "bold"))
submit_button.grid(row=3, column=1)



window.mainloop()
