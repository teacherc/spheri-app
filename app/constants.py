
WEATHERSTACK_CODES = {
    "intense": (392, 386, 377, 371, 365, 356, 350, 335, 314, 308, 305, 284, 281),
    "moody": (248, 143, 122, 119),
    "lovely": (116, 113),
    "chill": (296, 293),
    "moderate": (374, 362, 332, 329, 320, 317, 311, 302, 299, 260, 185, 182, 179, 176),
    "very_intense": (395, 389, 359, 338, 230, 227, 200),
    "whimsical": (368, 353, 326, 323, 266, 263),
    }

SPOTIFY_VALENCE = {
    "intense": (0.3, 0.6),
    "moody": (0.2, 0.5),
    "lovely": (0.7, 1),
    "chill": (0.5, 0.7),
    "moderate": (0.4, 0.6),
    "very_intense": (0, 0.3),
    "whimsical": (0.8, 1),
    }

BASE_URL = "https://api.spotify.com/v1/recommendations"

TOKEN_URL = "https://accounts.spotify.com/api/token"

ERROR_MESSAGES = {
                "INVALID_ZIPCODE" : 
                "Your zipcode is not valid. Please try again.",
                "INCOMPLETE_WEATHERSTACK_RESPONSE" : "The WeatherStack API returned an incomplete response. Please try again later.",
                "WEATHERSTACK_ZIP_ERROR" : "Weather API returned an incomplete response. Please re-enter a valid zipcode.",
                "SPOTIFY_API_ERROR" : "The Spotify API returned an error. Please try again later."
                  }
