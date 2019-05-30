import MySQLdb
from imutils import paths
import os

db = MySQLdb.connect('localhost', 'root', 'root1234', 'fashion')

def insertQuery(query):
    cursor = db.cursor()
    cursor.execute(query)

def lastInsertedId():
    cursor = db.cursor()
    cursor.execute("select LAST_INSERT_ID()")
    return cursor.fetchone()[0]

label_dict = {
    "red" : 1,
    "black" : 2,
    "shirt" : 3,
    "dress" : 4,
    "orange" : 5,
    "blue" : 6,
    "jeans" : 7,
}

IMG_DIR = "/Users/i506655/Downloads/datasets/dataset/"
imagePaths = list(paths.list_images(IMG_DIR))
for imagePath in imagePaths:
    print(imagePath)
    insertQuery("insert into apparel values(0,'%s')" % imagePath)
    img_id = lastInsertedId()
    labels = imagePath.split(os.path.sep)[-2].split("_")
    for l in labels:
        insertQuery("insert into has_labels values(%d,%d)" % (img_id, label_dict[l]))

db.commit()
db.close()
