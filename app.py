from flask import Flask ,request,jsonify,json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Resource, Api,fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://admin:admin@192.168.2.6:5432/db_sample'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']=True

db=SQLAlchemy(app)
ma=Marshmallow(app)

api = Api()
api.init_app(app)


#Table
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    email=db.Column(db.String)
    password=db.Column(db.String)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

#schema
class userSchema(ma.Schema):
    class Meta:
        fields=('id','name','email','password')

model=api.model('demo',{
    'name':fields.String('enter name'),
    'email':fields.String('enter email'),
    'password':fields.String('enter password')
})

user_schema=userSchema()
users_schema=userSchema(many=True)
# retrieve all data
@api.route('/get')
class getData(Resource):
    def get(self):
        user_data=User.query.all()
        result=users_schema.dump(user_data)
        return jsonify(result)

# add new data   
@api.route('/post')
class postData(Resource):
    @api.expect(model, validate=True)
    def post(self):
        usr=User(name=request.json["name"],email=request.json["email"],password=request.json["password"])
        db.session.add(usr)
        res=db.session.commit()
        return{'message':'data added to database'}

#   updates data
@api.route('/put/<id>')
class putData(Resource):
    @api.expect(model,validate=True)
    def put(self,id):
        user = User.query.get(id)
        user.name = request.json['name']
        user.email = request.json['email']
        user.password = request.json['password']
        db.session.commit()
        return {'message':'data updated'}


# delete data
@api.route('/delete/<id>')
class deleteData(Resource):
    def delete(self,id):
         user = User.query.get(id)
         db.session.delete(user)
         db.session.commit()
         return {'message':'data deleted'}

if __name__ == '__main__':
    app.run(debug=True)