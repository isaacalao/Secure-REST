import datetime, jwt, os, re, bcrypt
from fastapi import ( FastAPI, Depends, File, Response, HTTPException,  UploadFile, Header, Request, status )
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from . import database_handler 

load_dotenv('.env')
ALGORITHMS = os.getenv("ALGORITHMS")
SECRET = os.getenv("SECRET")
BLOWFISH_PREFIX = b'2a'

app = FastAPI(
    title="Secure REST API",
    description="A REST API that focuses on security tailored to initiate secure and reliable exchange of data from server to client or vice versa.",
    docs_url="/",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
token_auth_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def register_dep(username: str, password: str) -> tuple:
    if (re.match("^[a-zA-Z]{5,20}$", username)) and (re.match("^[a-zA-Z0-9]{5,30}$", password)):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') # Hash password with salt and convert to string
        Ok, Err = await database_handler.insert_user(username, hashed_password)
        if Ok:
            return (username, hashed_password)
        else:
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,detail=Err)

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                    "username": "Must be alphabetic and 5-20 characters long!",
                    "password": "Must be alphanumeric and 5-30 characters long!"
            }
        )

@app.post("/register-user")
async def register(user: tuple = Depends(register_dep)):
    """This endpoint is used to create a user."""
    username, password = user
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": f"User {username} created!",
        }
    )

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), request: Request = None):
    if form_data.username in database_handler.database['users']:
        
        hashed_password = database_handler.database['users'][form_data.username]['hashed_password'].encode('utf-8')

        if bcrypt.checkpw(form_data.password.encode('utf-8'), hashed_password):
            payload = database_handler.database['users'][form_data.username].copy()
            payload.__delitem__('hashed_password')
            #payload.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=2)})

            token = jwt.encode(
                payload=payload, 
                key=SECRET,
                algorithm=ALGORITHMS
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong password.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist.",
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message" : "Token created!",
            "access_token" : token
        }
    )

@app.get("/get-current-user")
async def get_user(token: str = Depends(token_auth_scheme), request: Request = None):
    """This endpoint shows the current authenticated user's information."""
    try:
        if not token == None:
            return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={ 
                        "user": jwt.decode(token, key=SECRET, algorithms=ALGORITHMS),
                        "user-agent": request.headers['user-agent']
                    }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access denied."
            )
    except jwt.exceptions.DecodeError:  
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
               detail="Expected JWT."
            )
    
@app.get("/get-all-users")
async def get_all_users(token: str = Depends(token_auth_scheme)):
    """This endpoint shows all of the registered users and their access level."""
    try:
        if jwt.decode(token, key=SECRET, algorithms=ALGORITHMS).get("access") == "All":
            return {
                    "users" : await database_handler.names_and_access() 
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access denied."
            )
    except jwt.exceptions.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expected JWT."
    )
