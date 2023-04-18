
#imports

import sqlite3
from sqlite3 import Error
import cv2
import numpy as np
import sys
import os
from PIL import Image





# creating a database if not existing
def create_connection(db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
            print(connected)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

# creating a table in the above DATABASE


def create_connection(db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "D:/db/CriminalDetails.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS People (
                                        ID text PRIMARY KEY,
                                        Name text NOT NULL,
                                        Age text NOT NULL,
                                        Gender text NOT NULL,
                                        CN VARCHAR(10) NOT NULL,
                                        Address text NOT NULL,
                                        CR text NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        # create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")



if __name__ == '__main__':
    create_connection("D:/db/CriminalDetails.db")
    main()


# face_data file below...

faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
imagePath = sys.argv[-1]


def insertOrUpdate(Id,Name,Age,Gen,CN,Address,Cr):
    conn=sqlite3.connect("D:/db/CriminalDetails.db")
    cup= conn.cursor()
    cmd="SELECT * FROM People WHERE ID="+str(Id)
    cursor=cup.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE People SET Name="+str(Name)+"WHERE ID="+str(Id)
        cmd2="UPDATE People SET Age="+str(Age)+"WHERE ID="+str(Id)
        cmd3="UPDATE People SET Gender="+str(Gen)+"WHERE ID="+str(Id)
        cmd4="UPDATE People SET CN="+str(CN)+"WHERE ID="+str(Id)
        cmd5="UPDATE People SET Address="+str(Address)+"WHERE ID="+str(Id)
        cmd6="UPDATE People SET CR="+str(Cr)+"WHERE ID="+str(Id)
        conn.execute(cmd)
    else:
        params = (Id,Name,Age,Gen,CN,Address,Cr)
        cmd="INSERT INTO People(ID,Name,Age,Gender,CN,Address,CR) Values(?, ?, ?, ?, ?, ?, ?)"
        cmd2=""
        cmd3=""
        cmd4=""
        cmd5=""
        cmd6=""
        conn.execute(cmd, params)

    conn.execute(cmd2)
    conn.execute(cmd3)
    conn.execute(cmd4)
    conn.execute(cmd5)
    conn.execute(cmd6)
    conn.commit()
    conn.close()

Id=input('Enter Criminal Id : ')
name=input('Enter Criminal Name : ')
age=input('Enter Criminal Age: ')
gen=input('Enter Criminal Gender : ')
CN=input('Enter Criminal Contact no. : ')
Address=input('Enter Address : ')
cr=input('Enter Criminal Criminal Records: ')
insertOrUpdate(Id,name,age,gen,CN,Address,cr)
a= input('upload image: ')
sampleNum=0
while(True):
    image = cv2.imread(a)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        sampleNum=sampleNum+1;
        cv2.imwrite("dataSet/User."+str(Id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.waitKey(100);
    cv2.imshow("Face",image);
    cv2.waitKey(1);
    if(sampleNum>10):
        break;


#facetrain file below....


#recognizer=cv2.createLBPHFaceRecognizer();
recognizer = cv2.face.LBPHFaceRecognizer_create()
path='dataSet'

def getImagesWithID(path):
    imagepaths=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    IDs=[]
    for imagepath in imagepaths:
        if ".DS_Store" in imagepath:
            print("Junk!")
        else:
            faceImg=Image.open(imagepath).convert('L');
            faceNp=np.array(faceImg,'uint8')
            ID=int(os.path.split(imagepath)[-1].split('.')[1])
            faces.append(faceNp)
            IDs.append(ID)
            cv2.imshow("training",faceNp)
            cv2.waitKey(10)
    return np.array(IDs),faces

IDs,faces=getImagesWithID(path)
recognizer.train(faces,IDs)
recognizer.save('recognizer/trainningData.yml')
cv2.destroyAllWindows()





#uploadrec file below......




# imagePath = sys.argv[-1]
# #faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
# faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# a=input('upload image : ')
# #rec=cv2.createLBPHFaceRecognizer();
# rec = cv2.face.LBPHFaceRecognizer_create()
# rec.read("recognizer/trainningData.yml")
# #font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX,0.4,1,0,1)

# fontface = cv2.FONT_HERSHEY_SIMPLEX
# fontscale = 1
# fontcolor = (0, 255, 0)
# #cv2.putText(im, str(Id), (x,y+h), fontface, fontscale, fontcolor) 

# def getProfile(id):
#     conn=sqlite3.connect("D:/db/CriminalDetails.db")
#     cmd="SELECT * FROM People WHERE ID="+str(id)
#     cursor=conn.execute(cmd)
#     profile=None
#     for row in cursor:
#         profile=row
#     conn.close()
#     return profile

# while(True):
#     image=cv2.imread(a);
#     gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#     faces=faceDetect.detectMultiScale(gray,1.3,5);
#     for(x,y,w,h) in faces:
#         cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
#         id,conf=rec.predict(gray[y:y+h,x:x+w])
#         print(id)
#         profile=getProfile(id)
#         if(profile!=None):
#             cv2.putText(image,"Name : "+str(profile[1]),(x,y+h+20),fontface, fontscale, fontcolor);
#             cv2.putText(image,"Age : "+str(profile[2]),(x,y+h+45),fontface, fontscale, fontcolor);
#             cv2.putText(image,"Gender : "+str(profile[3]),(x,y+h+70),fontface, fontscale, fontcolor); 
#             cv2.putText(image,"Contact no. : "+str(profile[4]),(x,y+h+95),fontface, fontscale, fontcolor);
#             cv2.putText(image,"Address  : "+str(profile[5]),(x,y+h+120),fontface, fontscale, fontcolor);
#             cv2.putText(image,"Criminal Records : "+str(profile[6]),(x,y+h+145),fontface, fontscale, fontcolor);
#         #else:
#             #cv2.putText(image,"Name : Unknown",(x,y+h+20),fontface, fontscale, fontcolor);
#             #cv2.putText(image,"Age : Unknown",(x,y+h+45),fontface, fontscale, fontcolor);
#             #cv2.putText(image,"Gender : Unknown",(x,y+h+70),fontface, fontscale, fontcolor);
#             #cv2.putText(image,"Contact no. : Unknown",(x,y+h+95),fontface, fontscale, fontcolor);
#             #cv2.putText(image,"Address : Unknown",(x,y+h+120),fontface, fontscale, fontcolor);
#             #cv2.putText(image,"Criminal Records : Unknown",(x,y+h+145),fontface, fontscale, fontcolor);
#     cv2.namedWindow('Face',cv2.WINDOW_NORMAL)
#     cv2.imshow("Face",image);
#     if(cv2.waitKey(1)==ord('q')):
#         break;
# cv2.destroyAllWindows()
