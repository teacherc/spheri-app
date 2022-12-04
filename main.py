import os
from flask import Flask
from flask import request, render_template
import re
import base64
import requests
import code_dict
import random
import sys
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
sys.path.insert(0, 'lib')

app = Flask(__name__)


def validate_zipcode(zipcode):
    return bool(re.search(r"^[0-9]{5}(-[0-9]{4})?$", zipcode))


def weather_from(valid_zipcode):
    # This function calls the WeatherStack API and stores the response
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    params = {"access_key": ACCESS_KEY, "query": valid_zipcode, "units": "f"}

    api_result = requests.get("http://api.weatherstack.com/current", params)
    weather = api_result.json()
    api_code = api_result.status_code

    weather_data = {"weather": weather, "api_code": api_code}

    return weather_data

def valence_function(weather_data):
    mood_valence_dict = {
    "intense": (0, 0.3),
    "moody": (0.2, 0.5),
    "lovely": (0.7, 1),
    "chill": (0.5, 0.7),
    "moderate": (0.4, 0.6),
    "very_intense": (0, 0.3),
    "whimsical": (0.8, 1),
    }
    code_dict = {
        "intense": (386, 377,371),
        "moody": (248, 143),
        "lovely": (116, 113),
        "chill": (296, 293),
        "moderate": (374, 362,317),
        "very_intense": (395, 389),
        "whimsical": (368, 353),
    }
    
    # This function uses the 'weather_code' to set the 'valence' parameter
    weather_code = weather_data["weather"]["current"]["weather_code"]
    valence = [mood_valence_dict[k] for k, v in code_dict.items() if weather_code in [v][0]]
    min_valence, max_valence = valence
    print(min_valence, max_valence)
    
    return min_valence, max_valence


def genre_function(weather_data):
    # This genre takes the 'feelslike' information to set the 'genre' parameter
    weather_genre = ""
    if int(weather_data["weather"]["current"]["feelslike"]) < 45:
        weather_genre = "jazz,classical"
    elif (
        int(weather_data["weather"]["current"]["feelslike"]) > 44
        and int(weather_data["weather"]["current"]["feelslike"]) <= 70
    ):
        weather_genre = "trip-hop,folk,chill,ambient"
    elif (
        int(weather_data["weather"]["current"]["feelslike"]) > 70
        and int(weather_data["weather"]["current"]["feelslike"]) <= 79
    ):
        weather_genre = "bossanova,soul,jazz"
    elif (
        int(weather_data["weather"]["current"]["feelslike"]) > 79
        and int(weather_data["weather"]["current"]["feelslike"]) < 100
    ):
        weather_genre = "synth-pop,indie-pop,soul"
    elif int(weather_data["weather"]["current"]["feelslike"]) < 99:
        weather_genre = "electronic,dance,dancehall,disco,breakbeat"
    return weather_genre


def authorization_spotify():
    # This function gets authorization from Spotify via client credentials
    # Establish variables
    url = "https://accounts.spotify.com/api/token"
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

    r = requests.post(url, headers=headers, data=data)
    token = r.json()["access_token"]

    return token


def spotify(token, valence, weather_genre):
    # This function generates the recommendation based on variables derived from the weather
    BASE_URL = "https://api.spotify.com/v1/recommendations"

    query_params = {
        "limit": 50,
        "market": "US",
        "seed_genres": weather_genre,
        "min_valence": valence[0],
        "max_valence": valence[1],
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


def say_recommendation(spotify_data, weather_data):
    # This function stores the recommendation in variables
    artist_name = spotify_data["spotify_response"]["tracks"][
        spotify_data["random_song"]
    ]["artists"][0]["name"]
    name_of_song = spotify_data["spotify_response"]["tracks"][
        spotify_data["random_song"]
    ]["name"]
    web_address = spotify_data["spotify_response"]["tracks"][
        spotify_data["random_song"]
    ]["external_urls"]["spotify"]
    album_cover_image = spotify_data["spotify_response"]["tracks"][
        spotify_data["random_song"]
    ]["album"]["images"][0]["url"]
    short_mp3_link = spotify_data["spotify_response"]["tracks"][
        spotify_data["random_song"]
    ]["preview_url"]
    feelslike = weather_data["weather"]["current"]["feelslike"]
    current_conditions = str(
        weather_data["weather"]["current"]["weather_descriptions"]
    ).strip("['']")
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
    valence = []
    weather_genre = ""
    token = []
    final_recommendation = {}
    spotify_data = {}

    if zipcode:
        if not validate_zipcode(zipcode):
            return render_template(
                "error2.html", test="Your zipcode is not valid. Please try again."
            )
        weather_data = weather_from(zipcode)
        if weather_data["api_code"] != 200:
            return render_template(
                "error2.html",
                test="Weather API returned an incomplete response. Please try again later.",
            )
        if "current" not in weather_data["weather"]:
            return render_template(
                "error2.html",
                test="Weather API returned an incomplete response. Please re-enter a valid zipcode.",
            )
        valence = valence_function(weather_data)
        weather_genre = genre_function(weather_data)
        token = str(authorization_spotify())
        spotify_data = spotify(token, valence, weather_genre)
        if spotify_data["spotify_status"] != 200:
            return render_template(
                "error2.html",
                test="The Spotify API returned an error. Please try again later.",
            )
        final_recommendation = say_recommendation(spotify_data, weather_data)

    else:
        return render_template("empty2.html")
    return render_template("form.html", zipcode=zipcode, **final_recommendation)


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="127.0.0.1", port=8080, debug=True)