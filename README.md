# fashionbot
## To do tasks
1. Finish UI
2. Convert recommender to API (Done)
3. Intergrate database with UI and recommender (Done)
4. Enrich color dataset (Done)
5. Apparel share feature
6. Initial Calibration of recommendation matrix

## Upload rules
1. Do not upload models or label bins(pull time becomes very high)
2. Segregate related content into seperate folders

## Steps to use project
1. Create models using the train.py and train_pattern.py ( Do not change model or labelbin names, dataset path can be changed)
 1. python ML/train.py -d dataset -m color_apparel.model -lb color_labels.lb -p plot_color_apparel.png
 2. python ML/train.py -d dataset -m color_apparel.model -lb color_labels.lb -p plot_pattern.png
2. Start the flask application by running "python app.py"

### [Link to datasets and models](https://drive.google.com/open?id=1imaiT9bOS0y4G5v2Xi_oawg5UrIbjbVT)
