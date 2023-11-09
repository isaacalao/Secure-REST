from fastapi import ( FastAPI, Depends, File, Response, HTTPException,  UploadFile, status )
from fastapi.security import ( APIKeyCookie, HTTPBearer, OAuth2PasswordBearer )
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from . import schema

app = FastAPI(
    title="Secure RESTFul API",
    description="A RESTful API that focuses on security tailored to initiate secure and reliable exchange of data from server to client or vice versa.",
    #docs_url="docs-something",
)
app.mount("/static", StaticFiles(directory="static"), name="static")

token_auth_scheme = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Keep in mind dynamic routes/endpoints should be below static ones

@app.get("/")
async def root():
    # HTML Content
    return HTMLResponse(
        content = 
            """
                <head>
                <title/>API Frontend</title>
                <link rel="icon"  href="/static/cloud-computing.png">
                <link rel="stylesheet" href="/static/style.css">
                <script type="text/javascript" src="/static/func.js"></script>
                </head>
                
                <body>
                <form action="/files/" enctype="multipart/form-data" method="post">
                    <input name="files" id="real-button" type="file" onchange="console.log(this.files)" multiple hidden>
                    <label class="mybutton" for="real-button">Choose Files</label>
                    <span id="file-chosen">No file chosen.</span>
                    
                    <input type="submit" class="mybutton" id="submit-button">    
                </form>
                </body>
            """
    )

@app.get("/pub-endpoint")
async def pub_endpoint_handler():
    """An access/authentication token is not required to access this endpoint."""

    return {
            "status": status.HTTP_200_OK, 
            "message": "Public endpoint."
    }

@app.get("/priv-endpoint")
async def priv_endpoint_handler(token: str = Depends(token_auth_scheme)):
    """An access/authentication token is required to access this endpoint."""
    if token.credentials == "admin":
        return {
                "status": status.HTTP_200_OK,
                "message": "Private endpoint",
                "token": token
        }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token!")

@app.post("/files/")
async def create_files(files: list[UploadFile] = File(description="Multiple files may be uploaded!")):
    file_name_and_size = [(file.filename, file.size) for file in files]
    return {
        "status": status.HTTP_200_OK,
        "file_sizes": [ file_name_and_size ]
    }

"""
@app.get("/priv-endpoint")
async def priv_endpoint_handler(token: str = Depends(token_auth_scheme)):
# An access/authentication token is required to access this endpoint.
    print(type(token))

    return { 
            "status": "",
            "message": "Private endpoint."
        }

@app.post("/demo")
async def demo_handler(demo: schema.Demo):
    return {"message": { "Demo returns": [demo.title, demo.body] }}
"""
