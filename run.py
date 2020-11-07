import os
import pprint
import traceback

import requests
import stdiomask

from reddit_service.authenticate import AuthenticateUser
from reddit_service.saved_posts import get_saved_posts

save_folder = "saved"

def process_image(data :dict):
    image_type = data["url"].split(".")[-1]
    print(image_type)
    resp = requests.get(data["url"])
    with open(os.path.join(save_folder, data["name"] + "." + image_type), "wb") as f:
        f.write(resp.content)

def process_video(data: dict):
    resp = requests.get(data["preview"]["reddit_video_preview"]["fallback_url"])
    with open(os.path.join(save_folder, data["name"] + ".mp4"), "wb") as f:
        f.write(resp.content)


if __name__ == "__main__":
    reddit_user_name = input("reddit_user_name: ")
    reddit_password = stdiomask.getpass("reddit_password: ")
    authenticate_user = AuthenticateUser(reddit_user_name, reddit_password)
    posts_limit = 100
    before_post = None
    if os.path.exists("latest_saved_post.txt"):
        with open("latest_saved_post.txt", "r") as f:
            before_post = f.read()
    
    if before_post:
        while True:
            posts = get_saved_posts(authenticate_user, before=before_post, posts_limit=posts_limit)
            for post in posts["data"]["children"]:
                print(post["data"]["name"])
                post_hint = post["data"].get("post_hint")
                if not post_hint:
                    continue
                try:
                    if "image" in post_hint:
                        process_image(post["data"])
                    if "video" in post_hint:
                        process_video(post["data"])
                except Exception as e:
                    traceback.print_exc()
            before_post = posts["data"]["children"][0]["data"]["name"]
            print("before_post", before_post)
            if len(posts["data"]["children"]) < posts_limit:
                print("data done")
                break
            
    
    else:
        after_post_name = None
        count=0
        while True:
            posts = get_saved_posts(authenticate_user, after=after_post_name, posts_limit=posts_limit)
            with open("latest_saved_post.txt", "w") as f:
                f.write(posts["data"]["children"][0]["data"]["name"])
            for post in posts["data"]["children"]:
                print(post["data"]["name"])
                post_hint = post["data"].get("post_hint")
                if not post_hint:
                    continue
                try:
                    if "image" in post_hint:
                        process_image(post["data"])
                    if "video" in post_hint:
                        process_video(post["data"])
                except Exception as e:
                    traceback.print_exc()
            after_post_name = posts["data"]["children"][-1]["data"]["name"]
            if len(posts["data"]["children"]) < posts_limit:
                print("data done")
                break
            