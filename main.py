from instagrapi import Client
import openai
import json
import time
import random
import argparse
import sys

def get_comments(api_key, number, hashtag, regarding):
    openai.api_key = api_key
    content_phrase = (f'erstelle {number} kommentare für instagram {hashtag} posts zum thema {regarding} in informal slang'
                      f' in einem structured data json format wie folgt ') + '{"number" : "comment"} ohne anderen text'
    print(content_phrase)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":content_phrase }]
    )

    return json.loads(completion.choices[0].message.content)

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
        except HTTPError:
            client = login_client()
            pass

def login_client():
    with open("creds", "r") as f:
        username, password, api_key = f.read().splitlines()
    print("Connecting to IG")
    new_client = Client()
    new_client.login(username, password)
    return new_client

parser = argparse.ArgumentParser(description="InstaComment")
parser.add_argument("--igusername", type=str, help="igusername")
parser.add_argument("--hashtag", type=str, help="hashtag")
parser.add_argument("--regarding", type=str, help="regarding")
parser.add_argument("--number", type=int, help="number", default=3)
parser.add_argument("--useapi", type=bool, help="use-api", default=False)
parser.add_argument("--maxintervalminutes", type=int, help="maxintervalminutes", default=1)

args = parser.parse_args()

print(f"started with {args}")
client = login_client()

if args.igusername is not None:
    print("args.igusername is not None")
    #user_id = client.user_id_from_username('mad.who0')
    user_id = client.user_id_from_username(args.igusername)
    print(user_id)
    medias = client.user_medias(user_id, 20)
elif args.hashtag is not None:
    print("args.hashtag is not None")
    hashtag = args.hashtag
    medias = client.hashtag_medias_recent(hashtag, 1)
else:
    print("ELSE")
    sys.exit()

if args.useapi:
    print("useapi true")
    comments = get_comments(api_key, args.number, args.hashtag, args.regarding)
else:
    print("ELSE - API")
    comments = ["SICK🔥", "STRONG🔥", "WOW 🔥🔥🔥"]
comment_media(client, medias, comments)