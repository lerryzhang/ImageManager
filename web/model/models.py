#coding=utf-8
from  web import db
ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    __tablename__ = 'i_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password=db.Column(db.String(255),unique=True)
    email = db.Column(db.String(255), unique=True)
    age=db.Column(db.Integer)
    sex=db.Column(db.Boolean)
    address=db.Column(db.String(255))
    tel=db.Column(db.String(255))
    lasttime=db.Column(db.DateTime)
    lastip=db.Column(db.String(255))
    createtime=db.Column(db.DateTime)
    status=db.Column(db.Integer)
    def __repr__(self):
        return '<User %r>' % (self.username)


class Image(db.Model):
    __tablename__ = 'i_image'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    storename=db.Column(db.String(255))
    filesize=db.Column(db.BigInteger)
    createtime = db.Column(db.DateTime)
    createuid=db.Column(db.Integer)
    createip=db.Column(db.String(255))
    content=db.Column(db.String(255))
    status=db.Column(db.Integer)

    def __repr__(self):
        return '<Iamge %r>' % (self.name)

#验证用户登录
def login(username,password,status):
    return User.query.filter(User.username == username, User.password == password, User.status == status).first()
#取出所有用户数据
def listAllUser():
    return User.query.all()
def getUser(id):
    return User.query.filter(User.id == id).first()
def saveUser(user):
    db.session.add(user)#添加到数据库
    db.session.commit()
def findIamge():
    return Image.query.all()
def getImage(id):
    return Image.query.filter(Image.id==id).first()
def saveImage(image):
    db.session.add(image)
    db.session.commit()
def delImage(image):
    db.session.delete(image)
    db.session.commit()
