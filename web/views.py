#coding=utf-8
from web import app
from flask import render_template,request,redirect,url_for,json,session,make_response
from werkzeug.utils import secure_filename
from form import forms
from rutil import rutil
from web.model.models import User,Image,login,listAllUser,getUser,saveUser,findIamge,saveImage,getImage,delImage
import datetime
import os

import sys

reload(sys)
sys.setdefaultencoding('utf8')


@app.before_request
def before_request():
    if session is not None and session.has_key('username') and session.has_key('uid') and session['username'] is not None and session['uid'] is not None:
        return
    else:
        account = request.cookies.get('account')
        if account is not None:
            accountArray = str(account).split('_')
            username = accountArray[0]
            uid = accountArray[1]
            session['username'] = username
            session['uid'] = uid
            return
        else:
            return redirect(url_for('main'))


@app.route('/')
def index():
   return redirect(url_for('listUser'))

@app.route('/main')
def main():
    registerform = forms.RegisterForm()
    loginform=forms.LoginForm()
    return render_template('login.html',registerform=registerform,loginform=loginform)


@app.route('/deleteUser',methods=['GET'])
def deleteUser():
    dict=None
    id=request.args.get("id")
    if id is not None:
        user=getUser(id)
        if user is not None:
            user.status=3
            saveUser(user)
            dict = {'mess': 'true'};
        else:
            dict = {'mess': 'false'};
    return json.dumps(dict)

@app.route('/editUser',methods = ['POST'])
def editUser():
    id=request.form.get("id")
    status=request.form.get("astatus")
    user=getUser(id)
    user.status=status
    saveUser(user)
    return redirect(url_for('listUser'))

@app.route('/listUser')
def listUser():
    users = listAllUser()
    return render_template('users.html', users=users)

@app.route('/login',methods = ['GET', 'POST'])
def submitLogin():
    form = forms.LoginForm()
    registerform = forms.RegisterForm()
    if form.validate_on_submit():
        username= request.form.get('username', None)
        remember_me = str(form.remember_me.data)
        password = rutil().md5(request.form.get('password', None))
        user=login(username,password,0)
        if user is not None:
            user.lasttime=datetime.datetime.now()
            user.lastip= request.remote_addr
            saveUser(user)
            session['uid']=user.id
            session['username']=user.username
            response = make_response(redirect(url_for('listUser')))
            if 'True'==remember_me:
                outdate = datetime.datetime.today() + datetime.timedelta(days=30)
                response.set_cookie('account', value='%s%s%s'%(user.username,'_',user.id), expires=outdate)
            return response
    return render_template('login.html', loginform=form,registerform=registerform)

@app.route('/logout')
def submitLogout():
    session.pop('username', None)
    session.pop('uid', None)
    dict = {'mess': 'true'};
    return json.dumps(dict)


@app.route('/register',methods = ['GET', 'POST'])
def submitRegister():
    form = forms.RegisterForm()
    loginfomr=forms.LoginForm()
    if form.validate_on_submit():
        username= request.form.get('username', None)
        password = request.form.get('password', None)
        email=request.form.get("email",None)
        sex = request.form.get("sex", None)
        age = request.form.get("age", None)
        tel = request.form.get("tel", None)
        address = request.form.get("address", None)
        user = User(username=username, email=email, password=rutil().md5(password),sex=sex,age=age,tel=tel,address=address,createtime=datetime.datetime.now(),status=1)
        saveUser(user)
        return render_template('registerOk.html')
    else:
       return render_template('login.html',loginfomr=loginfomr, registerform=form)

@app.route('/viewUser/<id>')
def viewUser(id):
    user=getUser(id)
    return render_template('user.html',user=user)


@app.route('/listImage',methods=['GET'])
def listImage():
    images=findIamge()
    return render_template('gallery.html',images=images)

@app.route('/upload/',methods=['POST'])
def upload():
    file=request.files['file']
    content=request.form.get("content")
    if content is None:
        content=""
    basepath = os.path.dirname(__file__)
    newFileName=rutil().getNewFileName(file.filename)
    upload_path = os.path.join(basepath, 'static\images\gallery', secure_filename(newFileName ))
    file.save(upload_path)
    image= Image(name=file.filename, storename=newFileName, filesize= len(file.read()),createtime=datetime.datetime.now(), createip=request.remote_addr,createuid=session['uid'],content=content)
    saveImage(image)
    dict= {'mess': 'true'};
    return json.dumps(dict)


@app.route('/deleteImage')
def deleteImage():
    id=request.args.get('id')
    dict=None
    if  id is None:
        dict={'mess':'false'}
    else:
        image=getImage(id)
        delImage(image)
        dict={'mess':'true'}
    return json.dumps(dict)








