from io import BytesIO
import os
from flask import Flask, redirect, render_template, request, send_file, send_from_directory, session
from werkzeug.utils import secure_filename 
import json
from PIL import Image
from bson import Binary
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER ='D:\\matrimonial site\\v6\\v6\\v6\\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = MongoClient('mongodb://localhost:27017/')
db = client['matrimonial']
collection = db['users']
# email_g=''
userl=''

@app.route('/')
def index():
     return render_template("index.html")

@app.route('/register')
def register():
     return render_template("Form.html")

@app.route('/login')
def login():
     return render_template("login.html")


@app.route('/' , methods=['GET', 'POST'])
def submit():
    
    
    
    whofor = request.form['for']
    full_name = request.form['full-name']
    gender =request.form['gender']
    dob= request.form['date-of-birth']
    martial_status = request.form['mst']
    height = request.form['height']
    weight = request.form['weight']
    blood_group = request.form['bloodgrp']
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']
    current_address = request.form['curradd']
    phone_no = request.form['phnno']
    email_g = request.form['email']
    native_place = request.form['place']
    religion = request.form['religion']
    community = request.form['caste']
    sub_community = request.form['SubCommunity']
    mother_tounge = request.form['lang']
    food_preference = request.form['foodpref']
    disability = request.form['disability']
#     distype = request.form['distype']

    
    photo = request.files['photo'] #######################
    if photo.filename == '':
        return 'No file selected'
    photo.save('uploads/' + photo.filename)
    photo_path='uploads/' + photo.filename


#     # Upload file flask
#     uploaded_img = request.files['photo']
#     # Extracting uploaded data file name
#     img_filename = secure_filename(uploaded_img.filename)
#     # Upload file to database (defined uploaded folder in static path)
#     uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
#     # Storing uploaded file path in flask session
#     a =  img_filename

    # Insert the image data into MongoDB
    


    qualification = request.form['education']
    occupation = request.form['occupation']
    college = request.form['college']
    work_company = request.form['workcompany']
    annual_income = request.form['annual-income']
    family_members = request.form['noOfFamily']
    mother = request.form['mother']
    mother_occ = request.form['mocc']
    father = request.form['father']
    father_occ = request.form['focc']
    guardian = request.form['guardian']
    living_status = request.form['livingstat']
    usr=''
    if(collection.find_one({'email':email_g})==None):
          user = {
               'whofor' : whofor,
               'fullname' : full_name,
               'gender' : gender,
               'dob' : dob,
               'martial_status' : martial_status,
               'height' : height,
               'weight' :weight,
               'blood_group':blood_group,
               'city':city,
               'state':state,
               'country':country,
               'current_address' : current_address,
               'phone_no' : phone_no,
               'email' : email_g,
               'native_place' : native_place,
               'religion' : religion,
               'community' : community,
               'sub_community' : sub_community,
               'mother_tounge' : mother_tounge,
               'food_preference' : food_preference,
               'disability' : disability,
               # 'distype' : distype,
               'qualification' : qualification,
               'occupation' : occupation,
               'college' : college,
               'work_company' : work_company,
               'annual_income' : annual_income,
               'family_members' : family_members,
               'mother' : mother,
               'mother_occ' : mother_occ,
               'father' : father,
               'father_occ' : father_occ,
               'guardian' : guardian,
               'living_status' : living_status,
               'name': photo.filename,
               
               'username':usr
          }
          session['g_email']=email_g
          collection.insert_one(user)
          return render_template('reg.html')
    else:
         return "email already exists"

@app.route('/regi', methods=['GET', 'POST'])
def regi():
     
          collection = db['creds']
          user=request.form['username']
          passw=request.form['password']

          
          email_g=session.get('g_email')


          if(collection.find_one({'username':user})==None):
               cred={
                    "username":user,
                    "password" : passw,
                    "email":email_g
               }
               collection.insert_one(cred)

               collection = db['users']
               collection.update_one({'email': email_g}, {'$set': {'username': user}})

               # ident={
               #      "username":user,
               # }
               # collection.insert_one(ident)

               return redirect('/login')
          else:
               return "username already exist"

@app.route('/dashboard')
def dashboard():
     if 'username' in session:
          logger=db['creds']
          userl=session.get('username')
          log=logger.find_one({'username':userl})
          d_email=log['email']

          collection = db['users']

          userd=collection.find_one({'email':d_email})
          # image_bytes = userd['data']
          if userd['gender']=='male':
               selected_entries = collection.find({'gender':'female'})
          else:
               selected_entries = collection.find({'gender':'male'})
          rendered_temp=render_template('dashboard.html', entries=selected_entries,users=userd)
          return rendered_temp 
     # ,send_file(BytesIO(image_bytes), mimetype='image/jpeg')
     #    return 'Logged in as ' + session['username']

     return 'You are not logged in dash'

@app.route('/uploads/<filename>')
def serve_image(filename):
    return send_from_directory('uploads', filename)

@app.route('/admindash')
def admindash():
     if 'username' in session:
          admin=db['admin']
          aduser=session.get('username')
          ad=admin.find_one({'username':aduser})
          collection = db['users']
          selected_entries = collection.find({})

          count = collection.count_documents({})
          count_m = collection.count_documents({'gender':'male'})
          count_f = collection.count_documents({'gender':'female'})

          return render_template('admin_dash.html', entries=selected_entries,users=ad,count=count,count_m=count_m,count_f=count_f)
     

@app.route('/profile')
def profile():
     if 'username' in session:
          logger=db['creds']
          userl=session.get('username')
          log=logger.find_one({'username':userl})
          d_email=log['email']

          collection = db['users']

          userd=collection.find_one({'email':d_email})
          img_p=userd['name']
          return render_template('profile.html',userp=userd,img_p=img_p)


@app.route('/checkin' , methods=['GET', 'POST'])
def checkin():

     logger=db['creds']
     userl=request.form['username']
     passwl=request.form['password']
     cred=logger.find_one({'username':userl})

     if cred==None:
          admin=db['admin']
          ad=admin.find_one({'username':userl})
          if ad['password']==passwl:
               session['username']=userl
               return redirect('/admindash')

     elif cred['password']==passwl:
          session['username'] = userl
          
          return redirect('/dashboard')
     return "incorrect username or password"

@app.route('/logout')
def logout():
    session.clear()  
    
    return redirect('/login')

     
     



if __name__ == '__main__':      
    
    app.run(host='0.0.0.0',port=5000,debug=True)