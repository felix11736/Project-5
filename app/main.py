from flask import Flask, jsonify, request
from decouple import config
import psycopg2
from flask_sqlalchemy import SQLAlchemy

DB_URI = (
    f"postgresql+psycopg2://{config('MB_DB_USER')}:{config('MB_DB_PASS')}"
    f"@{config('MB_DB_HOST')}:{str(config('MB_DB_PORT'))}/{config('MB_DB_DBNAME')}"
)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    telp = db.Column(db.String(14))


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/db_check")
def db_check():
    conn_pg = psycopg2.connect(
        host=config('MB_DB_HOST'),
        database=config('MB_DB_DBNAME'),
        user=config('MB_DB_USER'),
        password=config('MB_DB_PASS'),
        port=int(config('MB_DB_PORT')),
    )
    cur = conn_pg.cursor()
    return jsonify({"status": 200, "db": "connected"})


@app.route('/user', methods=["GET", "POST", "PUT", "DELETE"])
def user():
    if request.method == 'GET':
        users = Users.query.all()
        results = [
            {"id": u.id, "name": u.name, "city": u.city, "telp": u.telp}
            for u in users
        ]
        return jsonify(results)
    elif request.method == 'POST':
        user = Users(
            name=request.form['name'],
            city=request.form['city'],
            telp=request.form['telp']
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"status": "ok"})
    elif request.method == 'PUT':
        user = Users.query.filter_by(id=request.form['user_id']).first()
        if user:
            user.name = request.form.get('name', user.name)
            user.city = request.form.get('city', user.city)
            user.telp = request.form.get('telp', user.telp)
            db.session.commit()
            return jsonify({"status": "ok"})
    elif request.method == 'DELETE':
        user = Users.query.filter_by(id=request.form['user_id']).delete()
        db.session.commit()
        return jsonify({"status": "ok"})
    else:
        return 'Method not Allowed'


@app.route("/user/<id>", methods=['GET'])
def user_by_id(id):
    users = Users.query.filter_by(id=id)
    try:
        results = [{"id": u.id, "name": u.name, "city": u.city, "telp": u.telp}for u in users][0]
        return jsonify(results)
    except Exception:
        return jsonify({'error': "id not found"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
