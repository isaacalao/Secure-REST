import datetime, jwt, os
from fastapi import ( FastAPI, Depends, File, Form, Response, HTTPException,  UploadFile, Header, Request, status )
from fastapi.security import ( APIKeyCookie, HTTPBearer, HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer )
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from . import database_handler

load_dotenv('.env')
ALGORITHM = os.getenv("ALGORITHM")
SECRET = os.getenv("SECRET")


app = FastAPI(
    title="Secure RESTFul API",
    description="A RESTful API that focuses on security tailored to initiate secure and reliable exchange of data from server to client or vice versa.",
    #docs_url="docs-something",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
token_auth_scheme = HTTPBearer()


@app.get("/get-all-users")
async def get_all_users():
    """This endpoint shows all of the registered users and their access."""

    return { "users" : await database_handler.names_and_access() }

@app.get("/get-current-user")
async def get_user():
    """This endpoint shows the current authenticated user's information."""

    return ""

@app.post("/create-user")
#async def priv_endpoint_handler(token: str = Depends(token_auth_scheme)):
async def create_user(username: str, password: str, requests: Request):
    """This endpoint is used to create a user."""
    Ok, Err = await database_handler.insert_user(username, password)
    file_name_and_size = None

    if Ok:
        print(requests.headers)
        print(requests.headers['user-agent'])
        token = jwt.encode(payload=database_handler.database['users'][username], key=SECRET, algorithm=ALGORITHM)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": f"User {username} created!",
                "file_sizes": [ file_name_and_size ],
                "token": token

            }
        )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{Err}")


"""
@app.post("/demo")
async def demo_handler(demo: schema.Demo):
    return {"message": { "Demo returns": [demo.title, demo.body] }}
"""
