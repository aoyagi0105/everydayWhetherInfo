from flask import Flask
import requests

# LINE API 정보
LINE_ACCESS_TOKEN = 'WLHqXsJMK8wepoyn9Eg8TVMGy+P/3zpB3eLuF1LltSnfUYaTG+dEDX38BWGWR/UVwokEm9qJg00/FItP7A75nlD/XUG88wKswEWZAHJmd7fqGHgUK5fEhV9ILH6Wjli5qDS/Tv//jWOlKp9c5TjefQdB04t89/1O/w1cDnyilFU='
USER_ID = 'U603e79f8b1ba8adac666883a44e670c0'

# 날씨 API 정보
API_KEY = 'c1379b300675d9915bc9d9c077a9a406'
CITY = 'Osaka'


app = Flask(__name__)

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=kr"
    res = requests.get(url).json()
    weatherInfo = res["weather"]
    print(weatherInfo)

    weather_mains = {w["main"] for w in res["weather"]}
    if weather_mains & {"Rain", "Drizzle", "Thunderstorm"}:
        return f"오늘 {CITY}의 날씨는 {weatherInfo}. 우산을 챙기자"
    else: 
        return f"오늘 {CITY}의 날씨는 {weatherInfo}."

def send_line_message(msg):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type' : 'application/json',
        'Authorization' : f'Bearer {LINE_ACCESS_TOKEN}'
    }
    data = {
        'to': USER_ID,
        'messages': [{'type': 'text', 'text':msg}]
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code, response.text)

def daily_task():
    message = get_weather()
    send_line_message(message)

@app.route('/')
def index():
    return 'LINE 날씨 알림 서버 동작 중!'

if __name__ == '__main__':
    daily_task()