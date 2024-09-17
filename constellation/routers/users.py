import sys
from fastapi import APIRouter, Request, Cookie, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import datetime as dt
from jose import JWTError, jwt
from dotenv import dotenv_values

sys.path.append("../")
from matching import matching_user
from randomname.database import connection

config = dotenv_values("/Users/snaya/Matching/constellation/.env")

RSA_PUBLIC_KEY_BODY = config.get("RSA_PUBLIC_KEY_BODY")

SECRET_KEY = "-----BEGIN RSA PUBLIC KEY-----\n" \
            + RSA_PUBLIC_KEY_BODY \
            + "\n-----END RSA PUBLIC KEY-----"

ALGORITHM = "RS256"

router = APIRouter()

templates = Jinja2Templates(directory="templates")

router.mount("/Users/snaya/Matching/constellation/static", StaticFiles(directory="static"), name="static")

@router.get("/user/", response_class=HTMLResponse)
async def show_user_data(request: Request):
    
    access_token = request.cookies.get("ACCESS_TOKEN")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(access_token, SECRET_KEY, audience="account", algorithms=ALGORITHM) # type: ignore
        username: str = payload.get("sub") # type: ignore
        email: str = payload.get("email") # type: ignore
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_data = get_user_by_email(db_connection=connection, email=email)
    match_sys = matching_user(db_connection=connection, email=email)
    response = templates.TemplateResponse("user.html", {"request": request,
                                                    "user_fullname": user_data["full_name"], # type: ignore
                                                    "user_readname": user_data["read_fullname"], # type: ignore
                                                    "user_email": user_data["email"], # type: ignore
                                                    "hobby": user_data["hobby"], # type: ignore
                                                    "age": user_data["age"], # type: ignore
                                                    "user_birthday": user_data["birthday"], # type: ignore
                                                    "user_starsign": user_data["user_starsign"], # type: ignore
                                                    "gender": user_data["gender"], # type: ignore
                                                    "job": user_data["job"], # type: ignore
                                                    "income": user_data["income"], # type: ignore
                                                    "match_data": match_sys
                                                    })
    return response

def get_user_by_email(db_connection, email):
    with db_connection.cursor() as cursor:
        sql = f"""
        select ud.full_name, ud.read_fullname, ud.email, ud.hobby, ud.birthday ,ud.starsign,
        ud.job ,ud.gender, ud.income, ss.starsign as user_starsign
        from user_data as ud join starsign as ss on ud.starsign = ss.id  where ud.email = "{email}"
        """
        cursor.execute(sql)
        connection.commit()
    user_data = cursor.fetchone()

    birth = user_data.get("birthday")

    bd_data = birth.split('.')
    bd_object = dt.date(year=int(bd_data[0]), month=int(bd_data[1]), day=int(bd_data[2]))
    age_gap = dt.date.today() - bd_object
    age = round(age_gap.days / 365)
    user_data['age'] = age

    return user_data

if __name__ == "__main__":
    pass