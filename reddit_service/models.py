import datetime
from dataclasses import dataclass


@dataclass
class AuthenticationResponse:

    reddit_user_name: str
    authentication_token: str
    authentication_expiry_time: datetime.datetime
