from flask import Flask, render_template, request, session, redirect
from werkzeug import secure_filename
from ML import classify,recommender_system
from imutils import paths
import json
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/img/"

@app.route('/upload')
def upload_page():
   return render_template('image_upload.html')

@app.route('/wardrobe')
def wardrobe():
   return render_template('wardrobe.html', wardrobe = get_wardrobe_items())

@app.route('/recommend/<int:user_id>')
def recommend(user_id):
   return render_template('recommendations.html', recs = recommender_system.get_recommendations(user_id))

@app.route('/feedback')
def feedback():
   data = recommender_system.get_image_for_recommendation()
   return render_template('feedback_training.html',  imgId = data[0], src = data[1])

@app.route('/update_recomm', methods = ['GET'])
def update_recomm():
   id = request.args.get("imgId")
   val = request.args.get("adjVal")
   #perform update
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
      return redirect('/upload')

def get_wardrobe_items():
   username = ""
   if 'username' in session:
      username = session['username']
   user_folder = app.config['UPLOAD_FOLDER'] + username
   img_paths = paths.list_images(user_folder)
   return img_paths
        
if __name__ == '__main__':
   app.run(debug = True)