from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routers import users, login, logout

app = FastAPI()

app.mount("/Users/snaya/Matching/constellation/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(users.router)
app.include_router(login.router)
app.include_router(logout.router)

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})