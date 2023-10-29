# Secure-RESTful
A RESTful API implementation tailored to initiate secure and reliable exchange of data from a server to a client or vice versa. 

## Getting Started
Make sure you are in the correct directory (that means the directory where `.git` is)

1. Create and activate the python environment 
    ```bash
    python3 -m venv <name_of_env>
    source <name_of_env>/bin/activate
    ```
    Note: `<name_of_env>` can be whatever you name it to be, but `venv` is preferred. 

2. Install the dependencies from `requirements.txt`
    ```bash
    pip3 install -r requirements.txt
    ```

3. Run the webserver
    ```bash
    # Reloads after most recent change
    uvicorn secure_api.main:app --reload
    
    # No reload
    uvicorn secure_api.main:app

    # Make available on LAN (0.0.0.0 wildcard addr)
    uvicorn secure_api.main:app --host 0.0.0.0 --port 8000 --reload
    ```
4. Try interacting with the server using `curl`
    ```bash
    # Retrieve private IP addr on OSX
    ipconfig getifaddr en0
    # There's probably a similar way of doing this on other systems but I can't account for that :|
    ```

    ```bash
    curl -X 'GET' 'http://localhost:8000/<change_this_endpoint>' -H 'accept: application/json'
    ```
