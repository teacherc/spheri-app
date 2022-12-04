from flask import Flask
from flask import request, render_template
import re
import base64
import requests
import config
import code_dict
import random
import sys
sys.path.insert(0, 'lib')

app = Flask(__name__)


def validate_zipcode(zipcode):
    return bool(re.search(r"^[0-9]{5}(-[0-9]{4})?$", zipcode))


def weather_from(valid_zipcode):
    # This function calls the WeatherStack API and stores the response
    params = {"access_key": config.access_key, "query": valid_zipcode, "units": "f"}

    api_result = requests.get("http://api.weatherstack.com/current", params)
    weather = api_result.json()
    api_code = api_result.status_code

    weather_data = {"weather": weather, "api_code": api_code}

    return weather_data

def valence_function(weather_data):
    # This function uses the 'weather_code' to set the 'valence' parameter
    if str(weather_data["weather"]["current"]["weather_code"]) in code_dict.lovely_dict:
        min_valence = 0.7
        max_valence = 1
    elif (
        str(weather_data["weather"]["current"]["weather_code"])
        in code_dict.intense_dict
    ):
        min_valence = 0.3
        max_valence = 0.6
    elif (
        str(weather_data["weather"]["current"]["weather_code"]) in code_dict.moody_dict
    ):
        min_valence = 0.2
        max_valence = 0.5
    elif (
        str(weather_data["weather"]["current"]["weather_code"]) in code_dict.chill_dict
    ):
        min_valence = 0.5
        max_valence = 0.7
    elif (
        str(weather_data["weather"]["current"]["weather_code"])
        in code_dict.moderate_dict
    ):
        min_valence = 0.4
        max_valence = 0.6
    elif (
        str(weather_data["weather"]["current"]["weather_code"])
        in code_dict.very_intense_dict
    ):
        min_valence = 0
        max_valence = 0.3
    elif (
        str(weather_data["weather"]["current"]["weather_code"])
        in code_dict.whimsical_dict
    ):
        min_valence = 0.8
        max_valence = 1
    else:
        pass

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
    message = f"{config.client_id}:{config.client_secret}"
    messageBytes = message.encode("ascii")
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode("ascii")

    # Request authorization from API and return a token
    headers["Authorization"] = f"Basic {base64Message}"
    data["grant_type"] = "client_credentials"

    r = requests.post(url, headers=headers, data=data)
    token = r.json()["access_token"]

    return token


def spotify(token, min_valence, max_valence, weather_genre):
    # This function generates the recommendation based on variables derived from the weather
    BASE_URL = "https://api.spotify.com/v1/recommendations"

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
    min_valence = ""
    max_valence = ""
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
        min_valence, max_valence = valence_function(weather_data)
        weather_genre = genre_function(weather_data)
        token = str(authorization_spotify())
        spotify_data = spotify(token, min_valence, max_valence, weather_genre)
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
    app.run(debug=True)