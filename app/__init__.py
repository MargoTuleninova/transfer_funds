from flask import Flask
from app.logger import set_logger
from config import max_batch_len
from csv import writer
from psycopg2 import connect


logger = set_logger()
app = Flask(__name__)

conn = connect("dbname=bank user=margo host=0.0.0.0 port=55555 password=verystrong")
c = conn.cursor()

from app.routes import routes
app.register_blueprint(routes)
batch = []


@app.after_request
def metrics(response):
    # waiting for batch from 10 elements before writing
    if len(batch) < max_batch_len:
        batch.append(response)
    else:
        with open('metrics.csv', 'a', newline='') as f:
            csvwriter = writer(f)
            for i in range(max_batch_len):
                csvwriter.writerow(['HTTP Response', str(batch[i].status), str(batch[i].response)])
        batch[:] = []
    return response
