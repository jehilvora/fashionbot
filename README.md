# fashionbot
## To do tasks
1. Finish UI
2. Convert recommender to API
3. Intergrate database with UI and recommender
4. Enrich color dataset

## Upload rules
1. Do not upload models or label bins(pull time becomes very high)
2. Segregate related content into seperate folders

## Steps to use project
1. Create models using the train.py and train_pattern.py ( Do not change model or labelbin names, dataset path can be changed)
..1. python ML/train.py -d dataset -m color_apparel.model -lb color_labels.lb -p plot_color_apparel.png
..2. python ML/train.py -d dataset -m color_apparel.model -lb color_labels.lb -p plot_pattern.png
2. Start the flask application by running "python app.py"
