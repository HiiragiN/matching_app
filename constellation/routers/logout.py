from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import urllib.parse as parse
from dotenv import dotenv_values

# from routers.login import APP_CLIENT_ID, APP_BASE_URL, KEYCLOAK_BASE_URL_LOCALHOST, KEYCLOAK_REALM

router = APIRouter()

config = dotenv_values(".env")
APP_BASE_URL = config.get("APP_BASE_URL")
APP_CLIENT_ID = config.get("APP_CLIENT_ID")
APP_CLIENT_SECRET = config.get("APP_CLIENT_SECRET")
APP_REDIRECT_URI = config.get("APP_REDIRECT_URI")

KEYCLOAK_BASE_URL_LOCALHOST = config.get("KEYCLOAK_BASE_URL_LOCALHOST") 
KEYCLOAK_REALM = config.get("KEYCLOAK_REALM")

APP_LOGOUT_REDIRECT_URL = f"{APP_BASE_URL}/logout/callback"

LOGOUT_URL = f"{KEYCLOAK_BASE_URL_LOCALHOST}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/logout"

@router.get("/logout")
async def logout(request: Request) -> RedirectResponse:
    # This will do logout and redirect back to the application logout callback endpoint
    id_token = request.cookies.get("ID_TOKEN")
    get_param = parse.urlencode({"client_id": APP_CLIENT_ID,
                                "post_logout_redirect_uri": APP_LOGOUT_REDIRECT_URL,
                                "id_token_hint": id_token})

    # This will logout from Keyclaok and logged out page is served in keyclaok
    # get_param = parse.urlencode({"client_id": APP_CLIENT_ID})
    
    url = LOGOUT_URL + "?{}".format(get_param)

    return RedirectResponse(url)

@router.get("/logout/callback")
async def logout_cb(request: Request) -> RedirectResponse:
    response = RedirectResponse("/")
    
    response.delete_cookie("ID_TOKEN")
    response.delete_cookie("ACCESS_TOKEN")
    response.delete_cookie("REFRESH_TOKEN")
    response.delete_cookie("AUTH_STATE")
    return response