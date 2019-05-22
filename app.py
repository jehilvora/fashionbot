from flask import Flask, render_template, request
from werkzeug import secure_filename
import classify
import json
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/img"

@app.route('/upload')
def upload_page():
   return render_template('image_upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      final_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
      f.save(final_path)
      final_predictions = { "color" : classify.giveLabelPredictions(final_path, "color"),
      "pattern": classify.giveLabelPredictions(final_path, "pattern")}
      return json.dumps(final_predictions)
		
if __name__ == '__main__':
   app.run(debug = True)