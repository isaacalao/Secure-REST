# STEPS
1. Generate a 21-digit secret and store it in `.env`
```bash
 echo -ne "ALGORITHMS = HS256\nSECRET = $(python3 -c "import secrets; print(secrets.token_hex(21))")" > .env
```
* Running this command again will override the contents of `.env`

