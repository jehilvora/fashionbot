from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug import secure_filename
from ML import classify,recommender_system
import json
import os
import MySQLdb

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/img/"
app.secret_key = os.urandom(12)

db=MySQLdb.connect("localhost","root","root1234","fashion")

def getSingleValue(query):
   cursor = db.cursor()
   cursor.execute(query)
   return cursor.fetchone()

def getAllValues(query):
   cursor = db.cursor()
   cursor.execute(query)
   return cursor.fetchall()

def executeNonQuery(query):
   cur = db.cursor()
   cur.execute(query)
   db.commit()   

@app.route("/", methods=['GET'])
def home():
   messages = request.args.get('messages')
   #logged_in is the key in session variable for current login status
   if session.get("logged_in"):
      return redirect(url_for('wardrobe'))
   else:
      return render_template('login.html', messages = messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      username = request.form['username']
      psw = request.form['psw']
      reqPsw = getSingleValue("select password from users where Name = '%s'" % username)
      user_id = getSingleValue("select id from users where Name = '%s'" % username)
      if reqPsw != None and psw == reqPsw[0]:
            session['username'] = username
            session['logged_in'] = True
            session['user_ID'] = user_id[0]
            return redirect(url_for('wardrobe'))
      else:
         return render_template('login.html', messages="Wrong username or password")

@app.route('/logout', methods = ['GET'])
def logout():
   session['logged_in'] = False
   return render_template('login.html', messages = "Successfully logged out")


@app.route('/wardrobe')
def wardrobe():
   username = ""
   if 'username' in session:
      username = session['username']
   user_folder = app.config['UPLOAD_FOLDER'] + username
   wardrobe = recommender_system.get_wardrobe_items(user_folder)
   apparel_labels = {}
   for row in wardrobe:
      apparel_labels.setdefault(row[0], []).append(row[1])
   return render_template('wardrobe.html', apparel_labels = apparel_labels)

@app.route('/recommend/')
def recommend():
   return render_template('recommendations.html', recs = recommender_system.get_recommendations(int(session['user_ID'])))

@app.route('/feedback')
def feedback():
   data = recommender_system.get_image_for_recommendation()
   return render_template('feedback_training.html',  imgId = data[0], src = data[1])

@app.route('/update_recomm', methods = ['GET'])
def update_recomm():
   id = int(request.args.get("imgId"))
   val = int(request.args.get("adjVal"))
   recommender_system.adjust_matrix(id, val, int(session['user_ID']))
   result = recommender_system.get_image_for_recommendation()
   return json.dumps(result)
    
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      username = ""
      if 'username' in session:
         username = session['username']
      user_folder = app.config['UPLOAD_FOLDER'] + username
      if not os.path.exists(user_folder):
         os.makedirs(user_folder)
      final_path = os.path.join(user_folder, secure_filename(f.filename))
      f.save(final_path)
      predictions = classify.giveLabelPredictions(final_path, "color") + classify.giveLabelPredictions(final_path, "pattern")
      predictions = [x for x in predictions if x[1] > 0.6]
      recommender_system.add_user_item(final_path, predictions)
      return redirect('/')

@app.route('/delete', methods = ['GET'])
def deleteImage():
   path = request.args.get('path')
   recommender_system.remove_apparel(path)
   return redirect(url_for('home'))
        
if __name__ == '__main__':
   app.run(debug = True)
