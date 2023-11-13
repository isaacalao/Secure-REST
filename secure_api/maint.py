from fastapi import ( FastAPI, Depends, File, Form, Response, HTTPException,  UploadFile, Header, status )
from fastapi.security import ( APIKeyCookie, HTTPBearer, HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer )
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Secure RESTFul API",
    description="A RESTful API that focuses on security tailored to initiate secure and reliable exchange of data from server to client or vice versa.",
    #docs_url="docs-something",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
security = HTTPBasic()
token_auth_scheme = HTTPBearer()


# Keep in mind dynamic routes/endpoints should be below static ones 
@app.get("/")
async def root(header: str | None =  Header(default=None)):
    print(header)
    # HTML Content
    return HTMLResponse(
        content = 
            """
                <head>
                <title>API Frontend</title>
                <link rel="icon"  href="/static/cloud-computing.png">
                <link rel="stylesheet" href="/static/style.css">
                <script type="text/javascript" src="/static/func.js"></script>
                </head>
                <h1>Login</h1>
                <body>

                <form action="/files/" enctype="multipart/form-data" method="post">
                    <b>Password:</b> <br><input class="mybutton" name="password" id="ignore-hover" placeholder="Enter password here" type="password">
                    <br><br>
                    <input name="files" id="real-button" type="file" onchange="console.log(this.files)" multiple hidden>
                    <label class="mybutton" for="real-button">Choose Files</label>
                    <span id="file-chosen">No file chosen.</span>
                    
                    <input type="submit" class="mybutton" id="submit-button"> 
                </form>
                </body>
            """,
            headers={"Authorization": "Bearer admin"}
    )

@app.get("/pub-endpoint")
async def pub_endpoint_handler():
    """An access/authentication token is not required to access this endpoint."""

    return {
            "status": status.HTTP_200_OK, 
            "message": "Public endpoint."
    }

@app.post("/files")
#async def priv_endpoint_handler(token: str = Depends(token_auth_scheme)):
async def priv_endpoint_handler(files: list[UploadFile] = File(description="Multiple files may be uploaded!"), password: str = Form(), creds: str = Depends(token_auth_scheme)):
    """An access/authentication token is required to access this endpoint."""
    file_name_and_size = [(file.filename, file.size) for file in files]
    print(password)

    if password == "admin":
        return JSONResponse(content=
            {
                "status": status.HTTP_200_OK,
                "message": "Access granted to private endpoint",
                "file_sizes": [ file_name_and_size ],
                "token": password
            }, headers={"Authorization": f'Bearer {password}'}
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password!")

@app.get("/do-files")
async def handle(creds: str = Depends(token_auth_scheme)):
    return {
        "success", "tes"
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
