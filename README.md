![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white) ![Spotify](https://img.shields.io/badge/Spotify-1ED760?style=for-the-badge&logo=spotify&logoColor=white) ![Black](https://img.shields.io/badge/code%20style-black-black)[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) ![Self-taught](https://img.shields.io/badge/Self--taught-First%20Public%20Project-brightgreen_)

# spheri.app

## Table of Contents

- [Description](#description)
- [Motivation](#motivation)
- [Learning](#learning)
- [Installation](#installation)
- [Tests](#tests)
- [Usage](#usage)
- [Credits](#credits)
- [License](#license)


## Description

Public app: https://spheri.uk.r.appspot.com/

Spheri is a web app that uses local weather information to generate song recommendations. Someone experiencing thundersnow can expect a different recommendation than someone experiencing clear conditions at 72℉. 

This is my first public programming project. I decided to learn how to code when I was laid off from my startup job in mid-October 2022. I set the goal of deploying this app publicly by December 1, 2022.

### Motivation

I was the ten-year-old who begged to stay up past 11 pm so I could watch meteorologist Steve Pool talk about El Niño, dew points, and the jet stream. Even though I did not take up meterology as an adult, the weather has a big impact on my mood. I wanted to create something that would help me find new music that matches whatever weather vibes I'm experiencing.

This app solves a problem my wife and I have. There is so much music on Spotify, that it's hard to choose which new songs to listen to. I find myself listening to the same playlists over and over again.

### Learning

I also built this project so I could learn Python, Flask, git/GitHub, Bootstrap, APIs, unit testing, Google Cloud, and related technologies. I have been teaching myself to code since I was laid off from my startup job in mid-October 2022. After reading the first six chapters of *Automate the Boring Stuff with Python* and doing related exercises in *Python Exercises, Gently Explained*, I wanted to do my first public project.

## Repo Overview

- README.md
- LICENSE.md
- requirements.txt
- main.py
- test_main.py
- app.yaml
- code_dict.py
- templates
  - empty2.html
  - error2.html
  - form.html
  - layout.html
- assets
  - images
    - recommendation.png

## Installation

If you want to see how the app looks to users, you can visit [http://spheri.app]

To run in a local environment:

1. Create and activate a Python virtual environment (if you need to install Python 3.x, visit [https://www.python.org/downloads/]):

```shell
$ python -m venv venv
$ source venv/bin/activate
```

2. Update `pip` and install the required dependencies:

```shell
(venv) $ pip install -U pip
(venv) $ pip install -r requirements.txt
```

3. Create a '''config.py''' file with the proper keys

- Create a new app at [https://developer.spotify.com/dashboard/applications].
- Create a 'config.py' file in the main directory of where you've downloaded the code
- Fill in the client id and client secret:
```python
client_id = 'Spotify client ID'
client_secret = 'Spotify client secret'
```
- Sign up for a free WeatherStack API account [https://weatherstack.com/product]
- Add your WeatherStack access key to the config file:
```python
client_id = 'Spotify client ID'
client_secret = 'Spotify client secret'
access_key = 'WeatherStack access key'
```

4. Start the Flask server:

```shell
(venv) $ python main.py
 * Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 339-986-221
 ```

 5. Open a browser to the specified local address and port (Usually http://127.0.0.1:8080/. Voila! 

## Tests

Tests are located in ```test_main.py```. After you create your virtual environment and install the required packages, you can run ```test_main.py```. 

## Usage

A user can enter a valid U.S. zipcode, submit the zipcode, and receive a readout of local weather conditions as well as a song recommendation (via Spotify's recommendation API). A 30-second preview of the song can be accessed via the player. If a user clicks on the album art or the artist link, the corresponding Spotify track page will open.

![screenshot of Spheri recommendation](assets/images/recommendation.png)


## Credits

Useful tutorials:
- Cory Schafer's Flask tutorial [https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH]
- Bukola's Automate Spotify with Python [https://www.youtube.com/watch?v=7J_qcttfnJA]
- Freecodecamp's APIs for Beginners [https://www.youtube.com/watch?v=GZvSYJDk-us]
- Automate the Boring Stuff with Python [https://automatetheboringstuff.com/#toc]

## License

GNU General Public License v3.0 [https://choosealicense.com/licenses/gpl-3.0/]
