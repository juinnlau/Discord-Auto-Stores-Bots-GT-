import json
import os
import discord
import subprocess
import asyncio
import keyboard
import time
from pywinauto import Application
from discord.ext import commands
from pymongo import MongoClient
import dns.resolver

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

# Membaca nilai dari file config.json
with open('config.json') as config_file:
    config = json.load(config_file)

username = config['lucifer']['username']
password = config['lucifer']['password']
license  = config['lucifer']['license']

def open_app():
    try:
        path_aplikasi = r"C:\Users\juinn\Desktop\botku\Lucifer.exe"
        subprocess.Popen(path_aplikasi)
        print("Apps Opened Succesfully.")
    except FileNotFoundError:
        print("Apps not found.")
    except Exception as e:
        print(f"Something Errors when Opening the Apps: {str(e)}")

def login_app():
    time.sleep(1) 
    keyboard.write("1")
    time.sleep(1) 
    keyboard.press("enter")
    time.sleep(1) 
    keyboard.write(username) 
    time.sleep(1) 
    keyboard.press("enter")
    time.sleep(1) 
    keyboard.write(password) 
    time.sleep(1) 
    keyboard.press("enter")
    keyboard.write(license) 
    time.sleep(1) 
    keyboard.press("enter")
    

open_app() 
time.sleep(5) 
login_app() 
