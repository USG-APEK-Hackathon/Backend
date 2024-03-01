import requests
from decouple import config
from django.core.exceptions import ValidationError

GOOGLE_ID_TOKEN_INFO_URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"
GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def google_validate_id_token(id_token):
    response = requests.get(
        GOOGLE_ID_TOKEN_INFO_URL, params={"id_token": id_token}
    )

    if not response.ok:
        raise ValidationError("id_token is invalid.")

    audience = response.json()["aud"]

    if audience != config("GOOGLE_OAUTH2_CLIENT_ID"):
        raise ValidationError("Invalid audience.")

    return True


def google_get_access_token(code, redirect_uri):
    data = {
        "code": code,
        "client_id": config("GOOGLE_OAUTH2_CLIENT_ID"),
        "client_secret": config("GOOGLE_OAUTH2_CLIENT_SECRET"),
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

    if not response.ok:
        print(response.content)
        raise ValidationError("Failed to obtain access token from Google.")

    access_token = response.json()["access_token"]

    return access_token


def google_get_user_info(access_token):
    response = requests.get(
        GOOGLE_USER_INFO_URL, params={"access_token": access_token}
    )

    if not response.ok:
        raise ValidationError("Failed to obtain user info from Google.")

    return response.json()
