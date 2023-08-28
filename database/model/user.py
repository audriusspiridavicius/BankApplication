from itsdangerous import TimedJSONWebSignatureSerializer as Serializer    
from flask_login import UserMixin

from init import app,db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(300), nullable=False, default='default.png')
    
    
    
    def generate_password_reset_token(self,expire_time=360):
        token = Serializer(app.config['SECRET_KEY'], expire_time)
        
        token = token.dumps({"id":self.id}).decode('utf-8')
        
        return token
    
    def verify_password_reset_token(self, token):
        s = Serializer(app.config["SECRET_KEY"])
        
        user_id = s.loads(token)['id']
        
        return User.query.filter_by(id=user_id).first()
        
            
        
        
        