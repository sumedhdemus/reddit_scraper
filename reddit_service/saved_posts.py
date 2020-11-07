import requests

from configs.config import get_config
from reddit_service.authenticate import AuthenticateUser
from reddit_service.models import AuthenticationResponse

def get_saved_posts(authenticate_user: AuthenticateUser, posts_limit :int = None, before: str = None, after :str = None) -> list:
    """ gets saved posts from reddit
        limit : number of posts to get
        before : posts that come before a certain post name (inverse of time)
        after : posts that come after a post name (inverse of time)
    """

    config :dict = get_config()
    token_details :AuthenticationResponse = authenticate_user.authenticate()
    reddit_url = config["reddit_url"]
    saved_posts_endpoint = config["saved_posts_endpoint"].replace("username", token_details.reddit_user_name)
    headers = {"Authorization": f"bearer {token_details.authentication_token}", "User-Agent": f"RedditScraper/0.1 by {token_details.reddit_user_name}"}
    params = {
        "limit": posts_limit,
        "before": before,
        "after": after
    }
    response = requests.get(reddit_url + saved_posts_endpoint, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
