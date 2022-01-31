from flask import Flask, request, jsonify
from flask_cors import CORS
from itsdangerous import json
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
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

app.config["JWT_SECRET_KEY"] = "gr4rgr#21ff5frfuii"  
jwt = JWTManager(app)

@app.route("/")
def index():
    return 'index'

#Authentication
@app.route('/api/register', methods=['POST'])
def register():
    first_name = request.json.get('first_name', None)
    last_name = request.json.get('password', None)
    email = request.json.get('password', None)
    password = request.json.get('password', None)

    #Handle missing first name or last name or email or password
    if first_name is None or last_name is None or email is None or password is None:
        return {"error": "First Name or Last Name or Email or Password missing in body"}, 401

    cur = dbcon.cursor()

    #Check if user already exists 
    SQL = 'SELECT * FROM app_user WHERE email=%s'
    params = (email,)
    cur.execute(SQL, params)
    user = cur.fetchone()

    if user is not None:
        return {"error": "user with email already exists"}, 401
    
    #Create a new user - todo store hashed password
    SQL = '''
        INSERT INTO app_user(first_name, last_name, email, password)
        VALUES(%s, %s, %s, %s)
    '''
    params = (first_name, last_name, email, password)
    cur.execute(SQL, params)

    cur.close()

    return {}, 204

@app.route('/api/token', methods=['POST'])
def create_token():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    #Handle empty email or password
    if email is None or password is None:
        return {"error": "Email or Password missing in body"}, 401

    #Handle valid user check - todo use hashed passwords
    cur = dbcon.cursor()
    SQL = '''
        SELECT * FROM app_user 
        WHERE email=%s and password=%s 
    '''
    params = (email, password)
    cur.execute(SQL, params)

    user = cur.fetchone()
    cur.close()

    if user is None:
        return {"error": "Invalid credentials! User doesn't exist"}, 401

    access_token = create_access_token(identity=user[0])
    return jsonify(access_token=access_token) 


#Data
@app.route("/api/stock_news")
@jwt_required()
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
    app.run(debug=True)

    dbcon.close()