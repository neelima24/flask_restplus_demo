from flask import Flask , request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Resource, Api,fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://admin:admin@192.168.2.6:5432/db_sample'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=True
app.config['SECRET_KEY']=True

db=SQLAlchemy(app)
ma=Marshmallow(app)

api = Api()
api.init_app(app)


#Table
class user(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,not_null=True)
    email=db.Column(db.String)
    password=db.Column(db.String)

#schema
class userSchema(ma.Schema):
    class meta:
        fields=('id','name','email','password')

model=api.model('demo',{
    'name':fields.String('enter name'),
    'email':fields.String('enter email'),
    'password':fields.String('enter password')
})
        


user_schema=userSchema()
users_schema=userSchema(many=True)


@api.route('/get')
class getData(Resource):
    def get(self):
        return jsonify(users_schema.dump(user.query.all()))


@api.route('/post')
class postData(Resource):
    @api.expect('demo')
    def post(self):
        usr=user(name=request.get_json['name'],email=request.get_json['email'],password=request.get_json['password'])
        db.session.add(usr)
        db.session.commit()
        return{'message':'data added to database'}






if __name__ == '__main__':
    app.run(debug=True)