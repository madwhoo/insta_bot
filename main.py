from instagrapi import Client
import google.generativeai as genai
import openai
import json
import time
import random
import argparse
import sys


def get_comments(number, hashtag, regarding):
    genai.configure(api_key=api_key)
    content_phrase = (f"erstelle eine Liste im JSON schema mit {number} kommentare für instagram {hashtag} posts hinsichtlich {regarding} "
                      f"in informeller sprache und auf deutsch"
                      "Return: list[comment]")
    print(content_phrase)
    model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})
    completion = model.generate_content(content_phrase)
    print(completion.text)
    return json.loads(completion.text)


def comment_media(client, user_medias, comments):
    for i, media in enumerate(user_medias):
        try:
            time_sleep_random = random.randint(0, args.maxintervalminutes) * 60
            print(time_sleep_random)
            time.sleep(time_sleep_random)
            client.media_like(media.id)
            print(f"Liked post number {i + 1} of hashtag {media.id}")
            comment = random.choice(comments)
            client.media_comment(media.id, str(comment))
            print(f"Commented '{comment}' under post number {i + 1}")
        except Exception:
            client = login_client()
            pass


def login_client():
    print("Connecting to IG")
    new_client = Client()
    new_client.login(username, password)
    return new_client


parser = argparse.ArgumentParser(description="InstaComment")
parser.add_argument("--igusername", type=str, help="igusername")
parser.add_argument("--hashtag", type=str, help="hashtag")
parser.add_argument("--regarding", type=str, help="regarding")
parser.add_argument("--number", type=int, help="number", default=3)
parser.add_argument("--useapi", type=bool, help="useapi", default=False)
parser.add_argument("--maxintervalminutes", type=int, help="maxintervalminutes", default=1)

args = parser.parse_args()

print(f"started with {args}")
with open("creds", "r") as f:
    username, password, api_key = f.read().splitlines()
client = login_client()
amount = 20

if args.igusername is not None:
    print(f"Commenting {amount} of user {args.igusername}")
    user_id = client.user_id_from_username(args.igusername)
    print(user_id)
    medias = client.user_medias(user_id, amount)
elif args.hashtag is not None:
    print(f"Commenting {amount} for hashtag {args.hashtag}")
    hashtag = args.hashtag
    # private mobile api
    medias = client.hashtag_medias_recent_v1(hashtag, amount)
    # public web api
    # medias = client.hashtag_medias_recent_a1(hashtag, amount)
    # medias = client.hashtag_medias_recent(hashtag, amount)
else:
    print("Exiting script")
    sys.exit()

if args.useapi:
    print("Get comments from AI")
    comments = get_comments(args.number, args.hashtag, args.regarding)
else:
    print("Using default comments")
    comments = ["SICK🔥", "STRONG🔥", "WOW 🔥🔥🔥"]
comment_media(client, medias, comments)
