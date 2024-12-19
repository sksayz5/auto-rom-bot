import os
import requests
import json
from datetime import datetime
import pytz

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

def load_config():
    config_path = os.path.join(ASSETS_PATH, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as config_file:
            return json.load(config_file)
    else:
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")

def get_bot_token(token_file):
    """Retrieve the bot token from a file or prompt the user to enter it."""
    token_file = os.path.expanduser(token_file)
    if os.path.exists(token_file):
        with open(token_file, "r") as file:
            return file.read().strip()
    else:
        token = input("Enter your Telegram Bot Token: ").strip()
        with open(token_file, "w") as file:
            file.write(token)
        print(f"Token saved to {token_file}.")
        return token

def validate_bot_token(bot_token):
    """Validate the bot token by making a test API call."""
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Seems like your Telegram bot token is wrong.")
    return response.json()

def format_caption():
    """Generate the formatted text template."""
    today = datetime.now().strftime("%d/%m/%y")
    caption = f"""

#crDroid #spes #spesn #A15 #VIC #UNOFFICIAL #OSS
*crDroid 11.x | UNOFFICIAL | Android 15*
*Released:* _{today}_'

▪️Download
▪️Screenshots
▪️[Support Group](https://t.me/TanvirBuildsSupport)
▪️[Update Channel](https://t.me/Tanvir_CI)

*Changelog:*
• Type Here
• Type Here

*Notes:*
• Don't forget to backup your important data
• Use [PIF](https://t.me/TanvirBuilds/435) if needed
• Use official [OrangeFox](https://orangefox.download/device/spes) recovery
• Report bugs with proper logs
• If you like our work, consider [donating](https://github.com/Team-Remix/.github/blob/main/donation%2FDONATION.md) to support server costs
• This is an automatically generated post

*Credits:*
• All spes devs for resources
• All of my testers for testing
• Special thanks to God, Sun, Time, Love and Spes

*By* [@tanvirr007](https://t.me/tanvirr007)
*Follow* [@TanvirBuilds](https://t.me/TanvirBuilds)
*Join* [@TanvirBuildsSupport](https://t.me/TanvirBuildsSupport)
"""
    return caption

def get_Indian_time():
    """Get the current time and date in Indian Standard Time (BST)."""
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz)
    time = now.strftime("%I:%M %p")
    date = now.strftime("%d-%B-%Y")
    return time, date

def format_footer():
    """Generate the footer for the post with additional info."""
    time, date = get_Indian_time()
    footer = f"""
---
*Date:* `{date}`
*Time:* `{time} GMT+5:30 Indian (IST)`

*Note:* `This post was generated automatically by the bot and may contain pre-scheduled updates`
"""
    return footer

def send_photo_with_caption(bot_token, chat_id, photo_path, caption):
    """Send a photo with a caption to a Telegram chat."""
    if not os.path.exists(photo_path):
        raise FileNotFoundError(f"File '{photo_path}' not found.")

    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open(photo_path, "rb") as photo:
        response = requests.post(
            url,
            data={"chat_id": chat_id, "caption": caption, "parse_mode": "Markdown"},
            files={"photo": photo}
        )

    if response.status_code != 200:
        raise Exception(
            f"Failed to send photo. HTTP Status: {response.status_code}, Response: {response.text}"
        )
    return response.json()

if __name__ == "__main__":
    try:
        config = load_config()

        BOT_TOKEN = get_bot_token(config["token_file"])

        validate_bot_token(BOT_TOKEN)

        caption = format_caption()

        footer = format_footer()
        full_caption = caption + footer

        banner_path = os.path.join(ASSETS_PATH, config["banner_path"])

        response = send_photo_with_caption(BOT_TOKEN, config["chat_id"], banner_path, full_caption)
        print("Photo sent successfully. Response:", response)

    except FileNotFoundError as e:
        print(f"Error: {e}")

    except ValueError as e:
        print(f"Error: {e}")
        print("Please check your Telegram bot token and try again.")
        token_file_path = os.path.expanduser(config["token_file"])
        if os.path.exists(token_file_path):
            os.remove(token_file_path)
            print(f"The token file '{token_file_path}' has been removed. Please enter the correct token next time.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
