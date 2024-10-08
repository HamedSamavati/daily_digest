# a set of independent functions- without being a subset of a class
import random
import csv
import json
import datetime
from urllib import request


def get_random_quote(quotes_file="quotes.csv"):
    try:  # load motivational quotes from my csv file
        with open(quotes_file) as csvfile:
            quotes = [{'author': line[0],
                       'quote': line[1]} for line in csv.reader(csvfile, delimiter=',')]
    except Exception as e:  # use a default quote in case of any exception
        quotes = [{
            'author': 'Ralph Emerson',
            'quote': 'Skill to do comes of doing.'
        }]
    return random.choice(quotes)


def get_weather_forecast(coords={"lat": 50.445210, "long": -104.618896}):
    try:
        open_weather_api_key = "XXXXX"
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={coords["lat"]}&lon={coords["long"]}&appid={open_weather_api_key}&units=metric"
        data = json.load(request.urlopen(url))

        forecast = {
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "periods": list()
        }

        for period in data["list"][0:9]:
            forecast["periods"].append({
                "timestamp": datetime.datetime.fromtimestamp(period["dt"]),
                "description": period["weather"][0]["description"].title(),
                "temp": round(period["main"]["temp"]),
                "icon": f"https://openweathermap.org/img/wn/{period["weather"][0]["icon"]}.png"

            })
        return forecast

    except Exception as e:
        print(e)


def get_wikipedia_article():
    """to fetch a wikipedia article using the API"""
    try:
        data = json.load(request.urlopen('https://en.wikipedia.org/api/rest_v1/page/random/summary'))
        return {
            'title': data["title"],
            'url': data["content_urls"]["desktop"]["page"],
            'summary': data["extract"]}

    except Exception as e:
        print(e)


if __name__ == '__main__':
    ##### test get_rendom_quote() #####
    print("\n Testing quote generation...")
    quote = get_random_quote()
    print(f'The random quote is "{quote['quote']}"  -  {quote['author']}')

    quote = get_random_quote(quotes_file=None)
    print(f'The random quote is "{quote['quote']}"  -  {quote['author']}')

    #### test get_weather_forecast() ####

    forecast = get_weather_forecast()  # test with default location
    if forecast:
        print(f"Weather forecast for {forecast["city"]}, {forecast["country"]} is ... ")
        for period in forecast["periods"]:
            print(f" - {period["timestamp"]} | {period["temp"]}C | {period["description"]}")

    london = {"lat": 51.507351,
              "long": -0.127758}
    forecast = get_weather_forecast(coords=london)  # test with london
    if forecast:
        print(f"Weather forecast for {forecast["city"]}, {forecast["country"]} is ... ")
        for period in forecast["periods"]:
            print(f" - {period["timestamp"]} | {period["temp"]}C | {period["description"]}")

    invalid = {"lat": 12345,
               "long": 1234}
    forecast = get_weather_forecast(coords=invalid)  # test with an invalid location to check the exception
    if forecast:
        print(f"Weather forecast for {forecast["city"]}, {forecast["country"]} is ... ")
        for period in forecast["periods"]:
            print(f" - {period["timestamp"]} | {period["temp"]}C | {period["description"]}")

    ##### test get_wikipedia_article() ####
    print("\nTesting wiki random article generation ...")

    article = get_wikipedia_article()
    if article:
        print(f'The title: {article["title"]}\nThe url: {article["url"]}\nThe summary: {article["summary"]}')
