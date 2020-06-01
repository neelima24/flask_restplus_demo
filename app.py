from flask import Flask , request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Resource, Api,fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://admin:admin@localhost5432/db_sample.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=True
app.config['SECRET_KEY']=True

db=SQLAlchemy(app)
ma=Marshmallow(app)

api = Api(app)
api.init_app(app)


#Table
class user(db.Model):
    id=db.column(db.Integer,primary_key=True,autoincrement=True)
    name=db.column(db.String,not_null=True)
    email=db.column(db.String)
    password=db.column(db.String)

#schema
class userSchema(ma.Schema):
    class meta:
        fields=('id','name','email','password')
        model=api.model('demo',
        {
        'name':fields.String('Enter Name'),
        'email':fileds.String('Enter email'),
        'password':fields.String('Enter password')
        })

user_schema=userSchema()
users_schema=userSchema(many=True)


@api.route('/get', endpoint='todo_ep')
class getData(Resource):
    def get(self):
        return jsonify(users_schema.dump(user.query.all()))


@api.route('/post', endpoint='todo_ep2')
class postData(Resource):
    @api.expect(model)
    def post(self):
        usr=user(name=request.json['name'],email=request.json['email'],password=request.json['password'])
        db.session.add(usr)
        db,session.commit()
        return{'message':'data added to database'}






if __name__ == '__main__':
    app.run(debug=True)