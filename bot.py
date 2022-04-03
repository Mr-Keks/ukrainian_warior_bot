import subprocess
import sys
import pkg_resources

def check_requirements():
    required = {"telethon", "colorama", "getpass4", "requests", "asyncio"}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])

check_requirements()

import requests
import configparser
from os import system
from os.path import exists

import re
import asyncio
import random
from colorama import Fore
from getpass4 import getpass
from telethon import events
from telethon.sync import TelegramClient
from telethon.tl.types import InputReportReasonOther
from telethon.tl.functions.account import ReportPeerRequest


system("cls || clear")

red = Fore.RED
white = Fore.WHITE
blue = Fore.BLUE
yellow = Fore.YELLOW
lightgreen = Fore.LIGHTGREEN_EX

print(
    f"""
████████╗███████╗██╗░░░░░███████╗░██████╗░██████╗░░█████╗░███╗░░░███╗
╚══██╔══╝██╔════╝██║░░░░░██╔════╝██╔════╝░██╔══██╗██╔══██╗████╗░████║
░░░██║░░░█████╗░░██║░░░░░█████╗░░██║░░██╗░██████╔╝███████║██╔████╔██║
░░░██║░░░██╔══╝░░██║░░░░░██╔══╝░░██║░░╚██╗██╔══██╗██╔══██║██║╚██╔╝██║
░░░██║░░░███████╗███████╗███████╗╚██████╔╝██║░░██║██║░░██║██║░╚═╝░██║
░░░╚═╝░░░╚══════╝╚══════╝╚══════╝░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝
██████╗░███████╗██████╗░░█████╗░██████╗░████████╗███████╗██████╗░
██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
██████╔╝█████╗░░██████╔╝██║░░██║██████╔╝░░░██║░░░█████╗░░██████╔╝
██╔══██╗██╔══╝░░██╔═══╝░██║░░██║██╔══██╗░░░██║░░░██╔══╝░░██╔══██╗
██║░░██║███████╗██║░░░░░╚█████╔╝██║░░██║░░░██║░░░███████╗██║░░██║
╚═╝░░╚═╝╚══════╝╚═╝░░░░░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
    """
)

MESSAGES = [
    "The channel undermines the integrity of the Ukrainian state, spreads fake news, misleads people, thereby inciting aggression and calling for war between nations. It contains posts with threats against Ukrainian military personnel, which contribute to creating violent threats to the life and health of Ukrainian citizens. Under international law, this is regarded as terrorism.Therefore we ask You to block it as soon as possible!",
    "There are many posts with threats against the Ukrainian military. Lots of photos of the dead, blood and weapons. Block it!",
    "Propaganda of the war in Ukraine. Propaganda of murders of Ukrainians and Ukrainian soldiers. Block it!",
    "Dissemination of military personal data. Block the channel!",
    "Publication of military deaths, brutal killings, violence and hostilities. Please block the channel!",
    "The channel undermines the integrity of the Ukrainian state. Spreading fake news, misleading people. Block him as soon as possible!",
]

if not exists("config.ini"):
    print(
        red
        + "Отримати необхідні дані можна тут: from https://my.telegram.org/auth\n"
        + white
    )

    api_id = getpass(
        red
        + "┌─["
        + lightgreen
        + "Введіть ваш"
        + blue
        + "~"
        + white
        + "@API-ID"
        + red
        + "]\n" 
        + "└──╼ "
        + white
    )
    api_hash = getpass(
        red
        + "┌─["
        + lightgreen
        + "Введіть ваш"
        + blue
        + "~"
        + white
        + "@API-HASH"
        + red
        + "]\n"
        + "└──╼ "
        + white
    )
    name = "user.session"

    with open("config.ini", "w") as file:
        file.write("[Telegram]")
        file.write(f"\napi_id = {api_id}")
        file.write(f"\napi_hash = {api_hash}")
        file.write(f"\nusername = {name}")
else:
    config = configparser.ConfigParser()
    config.read("config.ini")
        
    api_id   = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    name = config['Telegram']['username']


def check_new_channels():
    if exists("channels.txt"):
        get_channels = requests.get('https://raw.github.com/Mr-Keks/ukrainian_warior_bot/main/daily_channels.txt').text.split()
        
        with open("channels.txt", "r") as file:
            old_channels = [channel.strip() for channel in file.readlines()]

        if len(old_channels) <= len(get_channels):
            files_difference = set(get_channels).difference(set(old_channels))

            if not files_difference:
                return None
            else:
                channels = [channel for channel in files_difference] 
                with open("channels.txt", "a") as file:
                    file.write("\n".join(channels))
                return channels
    else:
        get_channels = requests.get('https://raw.github.com/Mr-Keks/ukrainian_warior_bot/main/channels.txt').text.split()    
    
    with open("channels.txt", "w") as file:
        file.write("\n".join(get_channels))
    return get_channels


async def block_channels(channels):
    for channel in channels:
        await asyncio.sleep(random.randint(10, 15))
        try:
            result = await client(
                ReportPeerRequest(
                    peer=channel,
                    reason=InputReportReasonOther(),
                    message=random.choice(MESSAGES),
                )
            )
            print(white+"Скарга на канал", red+f"{channel[:-1]}", white+"відправлена", lightgreen+"успішно!")
        except Exception as e:
            print(white+"Не вдалося надіслати скаргу на канал", red+f"{channel}")


async def main():
    channels = check_new_channels()
    if channels:
        print("\nЗнайдені нові", red+"кацапські", white+"канали!")
        await block_channels(channels)
    else:
        print(white+"На даний момент нових кналів немає.")
if __name__ == "__main__":
    client = TelegramClient(name, api_id, api_hash)
    client.start()

    with client:
        print(lightgreen+"Роботу програми розпочато.\n")
        client.loop.run_until_complete(main())
    
    print(red + "\nРосійський військовий корабель, іди на хуй!\n"
        + blue + "Все буде", yellow + "Україна!", white)
    input()