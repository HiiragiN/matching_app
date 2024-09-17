import secrets
import urllib.parse as parse

import requests
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from dotenv import dotenv_values
# from keycloak import KeycloakOpenID

config = dotenv_values("../.env")

APP_BASE_URL = config.get("APP_BASE_URL")
APP_CLIENT_ID = config.get("APP_CLIENT_ID")
APP_CLIENT_SECRET = config.get("APP_CLIENT_SECRET")
APP_REDIRECT_URI = config.get("APP_REDIRECT_URI")

KEYCLOAK_BASE_URL_LOCALHOST = config.get("KEYCLOAK_BASE_URL_LOCALHOST")
KEYCLOAK_REALM = config.get("KEYCLOAK_REALM")

AUTH_BASE_URL = f"{KEYCLOAK_BASE_URL_LOCALHOST}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth"

TOKEN_URL = f"{KEYCLOAK_BASE_URL_LOCALHOST}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"

router = APIRouter()

@router.get("/login")
async def login() -> RedirectResponse:
    state = secrets.token_urlsafe(32)
    AUTH_URL = AUTH_BASE_URL + '?{}'.format(parse.urlencode({
        'client_id': APP_CLIENT_ID,
        'redirect_uri': APP_REDIRECT_URI,
        'scope': 'openid',
        'state': state,
        'response_type': 'code'
    }))
    response = RedirectResponse(AUTH_URL)
    response.set_cookie(key="AUTH_STATE", value=state)
    return response

def get_token(code):
    params = {
        'client_id': APP_CLIENT_ID,
        'client_secret': APP_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': APP_REDIRECT_URI,
        'code': code
    }
    token_response = requests.post(TOKEN_URL, params, verify=True)
    token = token_response.json()
    return token

@router.get("/login/callback")
async def auth(request: Request, code: str, state: str) -> RedirectResponse:
    if state != request.cookies.get("AUTH_STATE"):
        return {"error": "state_verification_failed"}  # type: ignore
    token = get_token(code)
    response = RedirectResponse("/user")
    # Store information in cookie.
    # Set following cookie values for security purpose, 
    # - Secure; (Limit Cookie access to connection over SSL. ) 
    # - HttpOnly (Avoid javascript access),
    # - SameSite=Strict (prevents some CSRF attacks)
    # - Domain=myapp.com, (Restrict which domaincan access the Cookies)
    # - Expires=<data time> (Cookie expiration timing)
    response.set_cookie(key="ACCESS_TOKEN", value=token.get("access_token"))
    response.set_cookie(key="ID_TOKEN", value=token.get("id_token"))
    response.set_cookie(key="REFRESH_TOKEN", value=token.get("refresh_token"))
    return response
    
if __name__ == "__main__":
    pass