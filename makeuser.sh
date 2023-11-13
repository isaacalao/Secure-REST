read -p "username: " testusername
read -p "password: " testpassword

curl -X 'POST' \
  "http://localhost:8000/register-user?username=$testusername&password=$testpassword" \
  -H 'accept: application/json' \
  -d ''\
  -s | json > out.json && bat out.json

curl -X 'POST' \
  'http://localhost:8000/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d "grant_type=&username=$testusername&password=$testpassword&scope=&client_id=&client_secret="\
  -s | json > out.json && bat out.json

read -p "Enter token: " testusertoken
auth_header="Authorization: Bearer $testusertoken"

curl -X 'GET' \
  'http://localhost:8000/get-current-user' \
  -H 'accept: application/json'\
  -H  "$auth_header"\
  -s | json > out.json 2>&1 && bat out.json

curl -X 'GET' \
  'http://localhost:8000/get-all-users' \
  -H 'accept: application/json'\
  -H  "$auth_header"\
  -s | json > out.json 2>&1 && bat out.json

rm out.json
