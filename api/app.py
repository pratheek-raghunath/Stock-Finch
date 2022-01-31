from flask import Flask, request
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os 

if os.environ.get('BASE_URI'):
    BASE_URI = os.environ.get('BASE_URI')
else:
    BASE_URI = 'localhost:5000'

DB_PASSWORD = 'x8Fpkla2CRb46MiCi467rp6Himr-D_VB'
DB_USER = 'davqufbg'
POSTGRES_DB = 'davqufbg'
DB_HOST = 'john.db.elephantsql.com'
dbcon = psycopg2.connect(user=DB_USER, password=DB_PASSWORD,
                            database=POSTGRES_DB, host=DB_HOST)

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return 'index'

@app.route("/api/stock_news")
def get_stock_news():
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    
    if not offset:
        offset = 0
    else:
        try:
            offset = int(offset)
        except:
            return {"error": "invalid offset"}, 400

    if not limit:
        limit = 10
    else:
        try:
            limit = int(limit)
        except:
            return {"error": "invalid limit"}, 400

    cur = dbcon.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    cur.execute('SELECT COUNT(*) AS c FROM stock_news')
    count = cur.fetchone()['c']

    SQL = '''
        SELECT * 
        FROM stock_news 
        ORDER BY publish_date DESC
        OFFSET %s
        LIMIT %s
    '''
    params = (offset,limit)

    cur.execute(SQL, params)
    stock_news_list = cur.fetchall()
    cur.close()

    stock_news_dict = {
        "has_prev": False,
        "prev": None,
        "has_next": False,
        "next": None,
        "data": stock_news_list,
    }
    
    if offset > 0:
        stock_news_dict['has_prev'] = True
        stock_news_dict['prev'] = BASE_URI + '/api/stock_news?offset=' + str(offset - limit) + '&limit=' + str(limit)

    if (offset + limit) < count:
        stock_news_dict['has_next'] = True
        stock_news_dict['next'] = BASE_URI + '/api/stock_news?offset=' + str(offset + limit) + '&limit=' + str(limit)

    return stock_news_dict

if __name__ == "__main__":
    app.run()

    dbcon.close()