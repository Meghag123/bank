import os 

base_dir=os.path.abspath(os.path.dirname(__file__))
class Config(object):
   SECRET_KEY=os.urandom(24).hex()
   #this is for database sqlite
   #SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(base_dir,'app.db')
   
   #for mysql we have
   SQLALCHEMY_DATABASE_URI="mysql+pymysql://flaskuser:flaskuser@localhost/userdb"
   SQLALCHEMY_TRACK_MODIFICATIONS=False
   
   #for mongodb connection
   MONGO_URI="mongodb://localhost:27017/custdb"
    
