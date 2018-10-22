To run postgres:

sudo docker run -d -p 55555:5432 -e POSTGRES_PASSWORD=verystrong -e POSTGRES_USER=margo -e POSTGRES_DB=bank postgres

Then:

psql -h 0.0.0.0 -p 55555 -U margo -d bank -a -f test_data.sql
Password: verystrong

Run app (port 5000):

python3 run.py

There are three tables in DB but methods for only two. Methods fot getting transfer history can be written in future.

Transfer is made as stored db procedure, can be found in test_data.sql

Sender should provide phone of receiver to transfer funds

Authorization is simplified, should use tokens of course

For metrics example, writing http responses to csv file in batches of ten records.

Examples:

curl 0.0.0.0:5000 --header "Authorization: Basic login=alice password=12345678" -v

curl 0.0.0.0:5000 -X POST --header "Authorization: Basic login=alice password=12345678" -F Receiver="79160000000" -F Amount=20 -v