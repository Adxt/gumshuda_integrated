import cv2
import numpy as np
import sqlite3
import sys

faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
imagePath = sys.argv[-1]


def insertOrUpdate(Id,Name,Age,Gen,CN,Address,Cr):
    conn=sqlite3.connect("C:/db/CriminalDetails.db")
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
