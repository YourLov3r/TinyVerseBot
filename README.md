🇷🇺 [Russian README](https://github.com/YourLov3r/TinyVerseBot/blob/master/README_RU.md)

# TinyVerse Bot 🌌

Script for automatization of tap-game TinyVerse

## Requirements

[![Python](https://img.shields.io/badge/python-%3E%3D3.10-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://www.python.org/)

## Features  

<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Supported</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SuperMegaCool Capybara intro</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Pre-Run Safety Checks</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Dust claim</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Add new stars to galaxy</td>
      <td><img src="https://img.shields.io/badge/Work_in_Progress-orange?style=flat-square"></td>
    </tr>
    <tr>
      <td>Apply boosts</td>
      <td><img src="https://img.shields.io/badge/Work_in_Progress-orange?style=flat-square"></td>
    </tr>
    <tr>
      <td>Script in .exe</td>
      <td><img src="https://img.shields.io/badge/Work_in_Progress-orange?style=flat-square"></td>
    </tr>
    <tr>
      <td>Night mode</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Proxy binding to session</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>User-Agent binding to session</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Auto-detect new .session and register it in bot</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Async working</td>
      <td>✅</td>
    </tr>
  </tbody>
</table>

## Why are we better than the rest of the public scripts?

### ✨ Capybara Intro (game changer, killer feature)

![Capybara Intro](https://github.com/YourLov3r/TinyVerseBot/blob/master/assets/Capybara_Intro.gif)

### 👥 Friendly community

We have created a friendly community where you can ask questions and get help.

### 🔗 We have a clear use of ref system

If you change the ref id to your own in the settings, that's what it will be. Our script does not prevent you from doing this, unlike some public scripts.

### 🚀 Regular updates

We update the script according to changes in the game.

## [Settings](https://github.com/YourLov3r/TinyVerseBot/blob/master/.env-example)

<table>
  <thead>
    <tr>
      <th>Settings</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>API_ID / API_HASH</td>
      <td>API credentials for Telegram API</td>
    </tr>
    <tr>
      <td>PLAY_INTRO</td>
      <td>True/False playing intro on script start (DON'T YOU DARE TO TURN THIS OFF)</td>
    </tr>
    <tr>
      <td>INITIAL_START_DELAY_SECONDS</td>
      <td>Delay range in seconds to use for a random delay when starting the session</td>
    </tr>
    <tr>
      <td>ITERATION_SLEEP_MINUTES</td>
      <td>How long the script will wait before starting the next iteration of the script (claiming, adding stars and e.t.c)</td>
    </tr>
    <tr>
      <td>USE_REF</td>
      <td>True/False the use of a referral to start the bot</td>
    </tr>
    <tr>
      <td>REF_ID</td>
      <td>Referrer ID</td>
    </tr>
    <tr>
      <td>SLEEP_AT_NIGHT</td>
      <td>True/False sleep at night</td>
    </tr>
    <tr>
      <td>NIGHT_START_HOURS</td>
      <td>Start hours range of the night</td>
    </tr>
    <tr>
      <td>NIGHT_END_HOURS</td>
      <td>End hours range of the night</td>
    </tr>
    <tr>
      <td>ADDITIONAL_NIGHT_SLEEP_MINUTES</td>
      <td>Additional minutes range to sleep at night</td>
    </tr>
    <tr>
      <td>CHECK_BOT_STATE</td>
      <td>True/False check bot state (is bot stopped by admins or not)</td>
    </tr>
    <tr>
      <td>CLAIM_DUST</td>
      <td>True/False auto-claim dust</td>
    </tr>
  </tbody>
</table>

## How to install 📚

Before you begin, make sure you have meet the [requirements](#requirements). It's really IMPORTANT, without these requiremenets, you can NOT install our script.

### Obtaining API Keys

1. Go to my.telegram.org and log in using your phone number.
2. Select "API development tools" and fill out the form to register a new application.
3. Record the API_ID and API_HASH provided after registering your application in the .env file.

Sometimes when creating a new application, it may display an error. It is still not clear what causes this, but you can try the solutions described on [stackoverflow](https://stackoverflow.com/questions/68965496/my-telegram-org-sends-an-error-when-i-want-to-create-an-api-id-hash-in-api-devel).

### Linux manual installation

```shell
git clone https://github.com/YourLov3r/TinyVerseBot.git
cd NotPixelBot
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install --only main
cp .env-example .env
nano .env
# Specify your API_ID and API_HASH, the rest is taken by default
# To exit from nano press Ctrl + O (will prompt you to save, accept) and then Ctrl + X
```

### Windows manual installation

```shell
git clone https://github.com/YourLov3r/TinyVerseBot.git
cd NotPixelBot
python -m venv .venv
.venv\Scripts\activate
pip install poetry
poetry install --only main
copy .env-example .env
# Then open .env in any text editor and specify your API_ID and API_HASH, the rest is taken by default
```

### Run the script

![NotPixel Intro](https://github.com/Dellenoam/NotPixelBot/blob/master/assets/NotPixel_Intro.gif)

#### Using start.bat

You can run the script using start.bat script, just execute it.

#### Manually

Before running the script, you ALWAYS need to activate the virtual environment and check for updates.

```shell
# Linux
source .venv\bin\activate
# Windows
.venv\Scripts\activate

# Linux/Windows
git pull
```

To run the script, use `python3 main.py` on Linux or `python main.py` on Windows.

Also, you can use flag `--action` or `-a` to quickly run the script with specified action.

```shell
# Linux
python3 main.py --action [1/2]
# Windows
python main.py --action [1/2]

# Or

# Linux
python3 main.py -a [1/2]
# Windows
python main.py -a [1/2]
```

Where [1/2] is:

    1 - Creates a session
    2 - Run bot

So for example if you want to create a session, you can run this command:

```shell
# Linux
python3 main.py --action 1
# Windows
python main.py --action 1

# Or

# Linux
python3 main.py -a 1
# Windows
python main.py -a 1
```

## Contacts

If you have any questions or suggestions, please feel free to contact us in comments.

[![Capybara Society Telegram Channel](https://img.shields.io/badge/Capybara%20Society-Join-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/capybara_society)