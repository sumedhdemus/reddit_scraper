import os
import json
import datetime

import requests

from reddit_service.models import AuthenticationResponse
from configs.config import get_config


class AuthenticateUser:
    """ class that holds data and methods required for authenticating self user """

    def __init__(self, reddit_user_name: str, reddit_password: str):
        
        if not isinstance(reddit_user_name, str):
            raise ValueError("reddit_user_name should be of type string")

        if not isinstance(reddit_password, str):
            raise ValueError("reddit_password should be of type string")

        self.reddit_user_name = reddit_user_name
        self.reddit_password = reddit_password

    def authenticate(
        self
    ) -> AuthenticationResponse:
        """
        Expects 4 values in env
        1. REDDIT_APP_CLIENT_ID: <your_app_client_id>
        2. REDDIT_APP_CLIENT_SECRET: <your_app_client_secret>
        3. REDDIT_USER_NAME: <your_user_name_for_reddit>
        4. REDDIT_PASSWORD: <your_reddit_password>
        Returns:
        AuthenticationResponse
        """

        

        reddit_app_client_id: str = os.getenv("REDDIT_APP_CLIENT_ID")
        reddit_app_client_secret: str = os.getenv("REDDIT_APP_CLIENT_SECRET")

        if not reddit_app_client_id:
            raise ValueError("REDDIT_APP_CLIENT_ID not present in environment")
        if not reddit_app_client_secret:
            raise ValueError("REDDIT_APP_CLIENT_SECRET not present in environment")

        config: dict = get_config()
        auth_url: str = config["reddit_auth_url"]
        endpoint: str = config["reddit_authentication_endpoint"]
        client_auth: requests.models.HTTPBasicAuth = requests.auth.HTTPBasicAuth(
            reddit_app_client_id, reddit_app_client_secret
        )
        post_data = {
            "grant_type": "password",
            "username": self.reddit_user_name,
            "password": self.reddit_password,
        }
        headers = {"User-Agent": f"PersonalClient/0.1 by {self.reddit_user_name}"}
        response: requests.models.Response = requests.post(
            auth_url + endpoint, auth=client_auth, data=post_data, headers=headers
        )
        response.raise_for_status()
        response: dict = response.json()
        authentication_expiry_time = datetime.datetime.now() + datetime.timedelta(
            seconds=response["expires_in"]
        )
        return AuthenticationResponse(
            authentication_token=response["access_token"],
            authentication_expiry_time=authentication_expiry_time,
            reddit_user_name=self.reddit_user_name,
        )
