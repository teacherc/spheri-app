import os
from flask import Flask
from flask import request, render_template
import re
import base64
import requests
import random
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, 'lib')

app = Flask(__name__)


def validate_zipcode(zipcode):
    return bool(re.search(r"^[0-9]{5}(-[0-9]{4})?$", zipcode))


def call_weather_api(valid_zipcode):
    # This function calls the WeatherStack API and stores the response
    access_key = os.getenv('ACCESS_KEY')
    params = {"access_key": access_key, "query": valid_zipcode, "units": "f"}

    api_result = requests.get("http://api.weatherstack.com/current", params)
    weather = api_result.json()
    api_code = api_result.status_code

    weather_data = {"weather": weather, "api_code": api_code}

    return weather_data

def assign_valence(weather_data):
    # This function uses the 'weather_code' to set the 'valence' parameter
    from constants import WEATHERSTACK_CODES, SPOTIFY_VALENCE
    weather_code = int(weather_data["weather"]["current"]["weather_code"])
    valence = [SPOTIFY_VALENCE[k] for k, v in WEATHERSTACK_CODES.items() if weather_code in v][0]
    min_valence = valence[0]
    max_valence = valence[-1]

    return min_valence, max_valence


def assign_genre(weather_data):
    # This genre takes the 'feelslike' information to set the 'genre' parameter
    weather_genre = ""
    feelslike = int(weather_data["weather"]["current"]["feelslike"]) 
    if -100 <= feelslike <15:
        weather_genre = "classical"
    if 15 <= feelslike < 40:
        weather_genre = "jazz"
    if 40 <= feelslike < 60:
        weather_genre = "trip-hop,ambient,chill"
    if 60 <= feelslike < 75:
        weather_genre = "folk"
    if 75 <= feelslike < 85:
        weather_genre = "bossanova,soul"
    if 85 <= feelslike < 100:
        weather_genre = "synth-pop,indie-pop,soul"
    if feelslike > 99:
        weather_genre = "electronic,dance,dancehall,disco,breakbeat"
        
    return weather_genre


def get_spotify_token():
    # This function gets authorization from Spotify via client credentials
    # Establish variables
    from constants import TOKEN_URL
    headers = {}
    data = {}

    # Encode as Base 64
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    message = f"{client_id}:{client_secret}"
    messageBytes = message.encode("ascii")
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode("ascii")

    # Request authorization from API and return a token
    headers["Authorization"] = f"Basic {base64Message}"
    data["grant_type"] = "client_credentials"

    r = requests.post(TOKEN_URL, headers=headers, data=data)
    token = r.json()["access_token"]

    return token


def call_spotify_api(token, min_valence, max_valence, weather_genre):
    # This function generates the recommendation based on variables derived from the weather
    from constants import BASE_URL
    query_params = {
        "limit": 50,
        "market": "US",
        "seed_genres": weather_genre,
        "min_valence": min_valence,
        "max_valence": max_valence,
        "min_instrumentalness": 0.5,
        "max_instrumentalness": 1,
    }

    response = requests.get(
        f"{BASE_URL}", params=query_params, headers={"Authorization": "Bearer " + token}
    )
    spotify_response = response.json()

    random_song = random.randint(0, len(spotify_response) - 1)

    spotify_status = response.status_code

    spotify_data = {
        "spotify_status": spotify_status,
        "spotify_response": spotify_response,
        "random_song": random_song,
    }
    
    return spotify_data


def assign_recommendations(spotify_data, weather_data):
    # This function stores the recommendation in variables
    artist_name = spotify_data["spotify_response"]["tracks"][spotify_data["random_song"]]["artists"][0]["name"]
    name_of_song = spotify_data["spotify_response"]["tracks"][spotify_data["random_song"]]["name"]
    web_address = spotify_data["spotify_response"]["tracks"][spotify_data["random_song"]]["external_urls"]["spotify"]
    album_cover_image = spotify_data["spotify_response"]["tracks"][spotify_data["random_song"]]["album"]["images"][0]["url"]
    short_mp3_link = spotify_data["spotify_response"]["tracks"][spotify_data["random_song"]]["preview_url"]
    feelslike = weather_data["weather"]["current"]["feelslike"]
    current_conditions = str(weather_data["weather"]["current"]["weather_descriptions"]).strip("['']")
    current_conditions = current_conditions.lower()
    city_name = weather_data["weather"]["location"]["name"]

    final_recommendation = {
        "name_of_song": name_of_song,
        "artist_name": artist_name,
        "web_address": web_address,
        "album_cover_image": album_cover_image,
        "short_mp3_link": short_mp3_link,
        "feelslike": feelslike,
        "current_conditions": current_conditions,
        "city_name": city_name,
    }

    return final_recommendation


@app.route("/")
def index():
    zipcode = request.args.get("zipcode", "")
    min_valence = ""
    max_valence = ""
    weather_genre = ""
    token = []
    final_recommendation = {}
    spotify_data = {}

    if zipcode:
        from constants import ERROR_MESSAGES
        if not validate_zipcode(zipcode):
            return render_template(
                "error.html", error_message=str(ERROR_MESSAGES["INVALID_ZIPCODE"])
            )
        weather_data = call_weather_api(zipcode)
        if weather_data["api_code"] != 200:
            return render_template(
                "error.html",
                error_message=str(ERROR_MESSAGES["INCOMPLETE_WEATHERSTACK_RESPONSE"])
            )
        if "current" not in weather_data["weather"]:
            return render_template(
                "error.html",
                error_message=str(ERROR_MESSAGES["WEATHERSTACK_ZIP_ERROR"])
            )
        min_valence, max_valence = assign_valence(weather_data)
        weather_genre = assign_genre(weather_data)
        token = str(get_spotify_token())
        spotify_data = call_spotify_api(token, min_valence, max_valence, weather_genre)
        if spotify_data["spotify_status"] != 200:
            return render_template(
                "error.html",
                error_message=str(ERROR_MESSAGES["SPOTIFY_API_ERROR"])
            )
        final_recommendation = assign_recommendations(spotify_data, weather_data)

    else:
        return render_template("empty.html")
    return render_template("form.html", zipcode=zipcode, **final_recommendation)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)