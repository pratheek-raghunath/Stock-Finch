from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
import psycopg2
import psycopg2.extras
import os 
from datetime import timedelta
import utils


BASE_URI = os.environ.get('BASE_URI')
DB_PASSWORD = os.environ['POSTGRES_PASSWORD']
DB_USER = os.environ['POSTGRES_USER']
POSTGRES_DB = os.environ['POSTGRES_DB']

#Connect to database
dbcon = psycopg2.connect(user=DB_USER, password=DB_PASSWORD,
                            database=POSTGRES_DB, host='postgresql')

app = Flask(__name__, static_folder="../build/static", template_folder="../build")
CORS(app)

#todo - increase token expiry time
app.config["JWT_SECRET_KEY"] = "gr4rgr#21ff5frfuii"  
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")

@app.route("/")
def index():
    return render_template('index.html')

#Authentication
@app.route('/api/register', methods=['POST'])
def register():
    first_name = request.json.get('first_name', None)
    last_name = request.json.get('last_name', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    phone = request.json.get('phone', None)

    #Handle missing first name or last name or email or password
    if first_name is None or last_name is None or email is None or password is None or phone is None:
        return {"error": "First Name or Last Name or Email or Password or Phone missing in body"}, 400

    cur = dbcon.cursor()

    #Check if user already exists 
    SQL = 'SELECT * FROM app_user WHERE email=%s'
    params = (email,)
    cur.execute(SQL, params)
    user = cur.fetchone()

    if user is not None:
        return {"error": "user with email already exists"}, 400
    
    #Create a new user - todo store hashed password
    SQL = '''
        INSERT INTO app_user(first_name, last_name, email, password, phone)
        VALUES(%s, %s, %s, %s, %s)
    '''
    params = (first_name, last_name, email, password, phone)
    cur.execute(SQL, params)

    cur.close()
    dbcon.commit()

    return {}

@app.route('/api/token', methods=['POST'])
def create_token():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    #Handle empty email or password
    if email is None or password is None:
        return {"error": "Email or Password missing in body"}, 400

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
        return {"error": "Invalid credentials! User doesn't exist"}, 400

    access_token = create_access_token(identity=user[0])
    return jsonify(access_token=access_token, first_name=user[1]) 


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
    

    stock_news_dict = {
        "has_prev": False,
        "prev": None,
        "has_next": False,
        "next": None,
        "data": stock_news_list,
    }
    
    if (offset - limit) >= 0:
        stock_news_dict['has_prev'] = True
        stock_news_dict['prev'] = BASE_URI + '/api/stock_news?offset=' + str(offset - limit) + '&limit=' + str(limit)

    if (offset + limit) < count:
        stock_news_dict['has_next'] = True
        stock_news_dict['next'] = BASE_URI + '/api/stock_news?offset=' + str(offset + limit) + '&limit=' + str(limit)

    app_user_id = get_jwt_identity()

    for i in range(len(stock_news_dict['data'])):
        news_id = stock_news_dict['data'][i]['id']

        SQL = '''
            SELECT * FROM news_archive WHERE news_id=%s AND app_user_id=%s
        '''
        params = (news_id, app_user_id)
        cur.execute(SQL, params)
        news_archive_item = cur.fetchone()

        if news_archive_item:
            stock_news_dict['data'][i]['is_archived'] = True
        else:
            stock_news_dict['data'][i]['is_archived'] = False

    cur.close()

    return stock_news_dict

@app.route('/api/stock_news/<int:id>')
@jwt_required()
def get_stock_news_item(id):
    cur = dbcon.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    SQL = '''
        SELECT * FROM stock_news WHERE id=%s
    '''
    params = (id,)
    cur.execute(SQL, params)
    stock_news_item = cur.fetchone()

    if not stock_news_item:
        return {"error": "Stock news item doesnt exist"}, 400

    app_user_id = get_jwt_identity()

    SQL = '''
            SELECT * FROM news_archive WHERE news_id=%s AND app_user_id=%s
        '''
    params = (id, app_user_id)
    cur.execute(SQL, params)
    news_archive_item = cur.fetchone()

    if news_archive_item:
        stock_news_item['is_archived'] = True
    else:
        stock_news_item['is_archived'] = False

    cur.close()

    return stock_news_item

@app.route('/api/news_archive', methods=['GET'])
@jwt_required()
def get_news_archive():
    app_user_id = get_jwt_identity()
    
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

    SQL = '''
        SELECT COUNT(*) AS c
        FROM stock_news s, news_archive n
        WHERE s.id = n.news_id AND n.app_user_id=%s
    '''
    params = (app_user_id,)

    cur.execute(SQL, params)
    count = cur.fetchone()['c']

    SQL = '''
        SELECT s.*
        FROM stock_news s, news_archive n
        WHERE s.id = n.news_id AND n.app_user_id=%s
        ORDER BY s.publish_date DESC
        OFFSET %s
        LIMIT %s
    '''
    params = (app_user_id, offset, limit)

    cur.execute(SQL, params)
    news_archive_list = cur.fetchall()

    news_archive_dict = {
        "has_prev": False,
        "prev": None,
        "has_next": False,
        "next": None,
        "data": news_archive_list,
    }
    
    if (offset - limit) >= 0:
        news_archive_dict['has_prev'] = True
        news_archive_dict['prev'] = BASE_URI + '/api/stock_news?offset=' + str(offset - limit) + '&limit=' + str(limit)

    if (offset + limit) < count:
        news_archive_dict['has_next'] = True
        news_archive_dict['next'] = BASE_URI + '/api/stock_news?offset=' + str(offset + limit) + '&limit=' + str(limit)

    for i in range(len(news_archive_dict['data'])):
        news_id = news_archive_dict['data'][i]['id']

        SQL = '''
            SELECT * FROM news_archive WHERE news_id=%s AND app_user_id=%s
        '''
        params = (news_id, app_user_id)
        cur.execute(SQL, params)
        news_archive_item = cur.fetchone()

        if news_archive_item:
            news_archive_dict['data'][i]['is_archived'] = True
        else:
            news_archive_dict['data'][i]['is_archived'] = False

    cur.close()

    return news_archive_dict

@app.route('/api/news_archive', methods=['POST'])
@jwt_required()
def add_news_archive():
    app_user_id = get_jwt_identity()

    news_id = request.json.get('news_id', None)

    if news_id is None:
        return {"error": "News Id missing in body"}, 400

    cur = dbcon.cursor()

    SQL = '''
        SELECT * FROM stock_news WHERE id=%s
    '''
    params=(news_id,)
    cur.execute(SQL, params)

    news = cur.fetchone()

    if news is None:
        return {"error": "News Id doesn't exist"}, 400

    SQL = '''
        SELECT * FROM news_archive WHERE news_id=%s AND app_user_id=%s
    '''
    params=(news_id, app_user_id)
    cur.execute(SQL, params)

    news_archive_item = cur.fetchone()

    if news_archive_item is not None:
        return {"error": "News Item already in user's archive"}, 400

    SQL = '''
        INSERT INTO news_archive(app_user_id, news_id)
        VALUES(%s, %s)
    '''
    params=(app_user_id, news_id)
    cur.execute(SQL, params)

    cur.close()
    dbcon.commit()

    return {}, 204

@app.route('/api/news_archive', methods=['DELETE'])
@jwt_required()
def remove_news_archive():
    app_user_id = get_jwt_identity()

    news_id = request.json.get('news_id', None)

    if news_id is None:
        return {"error": "News Id missing in body"}, 400

    cur = dbcon.cursor()

    SQL = '''
        SELECT * FROM news_archive WHERE news_id=%s AND app_user_id=%s
    '''
    params=(news_id,app_user_id)
    cur.execute(SQL, params)

    news_archive_item = cur.fetchone()

    if news_archive_item is None:
        return {"error": "News Item not in archive"}, 400

    SQL = '''
        DELETE FROM news_archive
        WHERE id=%s
    '''
    params=(news_archive_item[0],)
    cur.execute(SQL, params)

    cur.close()
    dbcon.commit()

    return {}, 204

@app.route('/api/search')
def search():
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
    
    query = request.args.get('query', '')
    query = query.split(' ')[0]
    if not query.isalnum():
        return {"error": "invalid query"}, 400
    query_prefixed = query + ':*'
    
    cur = dbcon.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    SQL = '''
        SELECT count(*)
        FROM (SELECT com.id AS cid,
                    com.name AS cname,
                    cd.nse AS nse,
                    stor.name AS sname,
                    to_tsvector(com.name) ||
                    to_tsvector(stor.name) ||
                    to_tsvector(cd.bse) ||
                    to_tsvector(cd.nse) ||
                    to_tsvector(cd.series) ||
                    to_tsvector(cd.isin) ||
                    to_tsvector(coalesce(string_agg(DISTINCT cm.name, ' '), '')) ||
                    to_tsvector(coalesce(string_agg(DISTINCT si.name, ' '), '')) AS document
            FROM company com JOIN "security" sec ON com.id = sec.company_id
                            JOIN sector stor ON sec.sector_id  = stor.id
                            JOIN company_details cd ON com.id = cd.company_id
                            JOIN company_management cm ON com.id = cm.company_id
                            JOIN stock_index_constituent sic ON sic.security_id = sec.id
                            JOIN stock_index si ON si.id = sic.stock_index_id
            GROUP BY com.id, com.name, stor.name, cd.bse, cd.nse, cd.series, cd.isin) p_search 
        WHERE p_search.document @@ to_tsquery(%s)
    '''

    params = (query_prefixed,)
    cur.execute(SQL, params)
    count = cur.fetchone()['count']

    SQL = '''
        SELECT cid, cname, nse, sname
        FROM (SELECT com.id AS cid,
                    com.name AS cname,
                    cd.nse AS nse,
                    stor.name AS sname,
                    to_tsvector(com.name) ||
                    to_tsvector(stor.name) ||
                    to_tsvector(cd.bse) ||
                    to_tsvector(cd.nse) ||
                    to_tsvector(cd.series) ||
                    to_tsvector(cd.isin) ||
                    to_tsvector(coalesce(string_agg(DISTINCT cm.name, ' '), '')) ||
                    to_tsvector(coalesce(string_agg(DISTINCT si.name, ' '), '')) AS document
            FROM company com JOIN "security" sec ON com.id = sec.company_id
                            JOIN sector stor ON sec.sector_id  = stor.id
                            JOIN company_details cd ON com.id = cd.company_id
                            JOIN company_management cm ON com.id = cm.company_id
                            JOIN stock_index_constituent sic ON sic.security_id = sec.id
                            JOIN stock_index si ON si.id = sic.stock_index_id
            GROUP BY com.id, com.name, stor.name, cd.bse, cd.nse, cd.series, cd.isin) p_search 
        WHERE p_search.document @@ to_tsquery(%s)
        ORDER BY cname
        OFFSET %s
        LIMIT %s;
    '''

    params = (query_prefixed, offset, limit)
    cur.execute(SQL, params)

    search_results = cur.fetchall()

    cur.close()

    if len(search_results) == 0:
        return {"error": "No results found"}, 404

    search_dict = {
        "has_prev": False,
        "prev": None,
        "has_next": False,
        "next": None,
        "results": search_results,
    }
    
    if (offset - limit) >= 0:
        search_dict['has_prev'] = True
        search_dict['prev'] = BASE_URI + '/api/search?query=' + query + '&offset=' + str(offset - limit) + '&limit=' + str(limit)

    if (offset + limit) < count:
        search_dict['has_next'] = True
        search_dict['next'] = BASE_URI + '/api/search?query=' + query + '&offset=' + str(offset + limit) + '&limit=' + str(limit)

    return search_dict

@app.route('/api/company/<int:id>')
def get_company(id):
    cur = dbcon.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    SQL = '''
        SELECT c.name AS name, st.name AS sector, s.id AS security_id
        FROM company c JOIN security s on c.id = s.company_id
                       JOIN sector st on s.sector_id = st.id
        WHERE c.id=%s
    '''
    params = (id,)
    cur.execute(SQL, params)
    company_dict = cur.fetchone()

    if not company_dict:
        cur.close()
        return {"error": "Company does not exist"}, 400

    security_id = company_dict['security_id']
    del company_dict['security_id']

    SQL = '''
        SELECT *
        FROM company_details
        WHERE company_id=%s
    '''
    params = (id,)
    cur.execute(SQL, params)
    company_details_dict = cur.fetchone()
    utils.remove_attr(company_details_dict)
    company_dict['details'] = company_details_dict

    SQL = '''
        SELECT *
        FROM company_management
        WHERE company_id=%s
    '''
    params = (id,)
    cur.execute(SQL, params)
    company_dict['management'] = []
    for manager in cur.fetchall():
        utils.remove_attr(manager)
        company_dict['management'].append(manager)

    SQL = '''
        SELECT *
        FROM company_overview
        WHERE company_id=%s
    '''
    params = (id,)
    cur.execute(SQL, params)
    company_overview_dict = cur.fetchone()
    utils.remove_attr(company_overview_dict)
    company_dict['overview'] = company_overview_dict

    SQL = '''
        SELECT si.name AS name
        FROM stock_index si JOIN stock_index_constituent sic ON si.id = sic.stock_index_id
        WHERE security_id=%s
    '''
    params = (security_id,)
    cur.execute(SQL, params)

    indices_list = cur.fetchall()

    company_dict['included_in'] = []
    for index in indices_list:
       company_dict['included_in'].append(index['name']) 

    cur.close()

    return company_dict
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

    dbcon.close()

