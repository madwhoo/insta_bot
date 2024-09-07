from time import sleep

from instagrapi import Client
from datetime import datetime
import google.generativeai as genai
#import openai
import json
import time
import random
import argparse
import sys
#import os

api_key = ""

class InstaHandler:

    def __init__(self, name, igusername, hashtag, regarding, number, useapi, maxintervalminutes):
        self.name = name
        self.igusername = igusername
        self.regarding = regarding
        self.number = number
        self.hashtag = hashtag
        self.useapi = useapi
        self.maxintervalminutes = maxintervalminutes

        self.comments = ["SICK🔥", "STRONG🔥", "WOW 🔥🔥🔥"]
        self.creds = ["creds_funkerin", "creds_krup", "creds_macker", "creds_frontler"]
        self.login_creds_dict = {}

    def run(self):
        pass

    def get_comments(self, number, hashtag, regarding):
        print(f"Using api_key : '{api_key}'")
        genai.configure(api_key=api_key)
        content_phrase = (
            f"erstelle eine Liste im JSON schema mit {number} kommentare für instagram '{hashtag}' posts hinsichtlich {regarding} "
            f"in Umgangssprache und auf deutsch "
            "Return: list[comment]")
        print(content_phrase)
        model = genai.GenerativeModel('gemini-1.5-flash-latest',
                                      generation_config={"response_mime_type": "application/json"})
        completion = model.generate_content(content_phrase)  # , request_options={"timeout": 120})
        print(completion.text)
        return json.loads(completion.text)

    def comment_media(self, client, user_medias):
        for i, media in enumerate(user_medias):
            time_sleep_random = random.randint(self.maxintervalminutes, self.maxintervalminutes + 60) * 5
            print(f"{datetime.now()} - Sleeping: '{time_sleep_random}'sec")
            time.sleep(time_sleep_random)
            print(f"{datetime.now()} - Done Sleeping")
            client.media_like(media.id)
            print(f"Liked post number {i + 1} of hashtag {media.id}")
            comment = random.choice(self.comments)
            client.media_comment(media.id, str(comment))
            print(f"Commented '{comment}' under post number {i + 1}")

    def login_client(self, attempts=0):
        print("Connecting to IG")
        if attempts < 3:
            user, password = random.choice(list(self.login_creds_dict.items()))
            print(f"Using login for: {user}")
            try:
                new_client = Client()
                new_client.login(user, password)
                return new_client
            except Exception:
                attempts = + 1
                sleep(300)
                self.login_client(attempts)
        else:
            print(f"Logging attempts exceeded. Exiting..")
            sys.exit()


    def load_creds(self):
        global api_key
        for cred in self.creds:
            with open(cred, "r") as f:
                username, password = f.read().splitlines()
            self.login_creds_dict[username] = password
        with open("creds_api", "r") as f:
            api_key = f.read().strip()

