import json
from model.util import group
from model.db import mongo
from datetime import datetime,timedelta

# name,gender,birth,height,weight

def getmofriend(friend_ids):
    return list(mongo.db.user.aggregate(
                [
                    {
                        "$match": {"id": {"$in": friend_ids}},
                    },
                    {"$unset": ["_id","password","friend","hide_friend"]},
                ]
            ))

# def addpeople(uid,name,gender,birth,height,weight,disease_id):
#     return list(mongo.db.people.insert_one({"uuid":uid,"name":name,"gender":gender,"birth":birth,"height":height,"weight":weight,"disease_id":disease_id}))

# def findname(name):
#     return list(mongo.db.people.find({"name":name},{"_id":0}))

# def finduid(uid):
#     return list(mongo.db.people.find({"uuid":uid},{"_id":0}))

# def editpeople(uid,name,gender,birth,height,weight,disease_id):
#     return mongo.db.people.update_one({"uuid":uid},{"$set": { "name":name,"gender":gender,"birth":birth,"height":height,"weight":weight,"disease_id":disease_id }})

# def findTherapist():
#     return list(mongo.db.user.find({"permission":2},{"_id":0}))

# def findTherapistWork(t_id):
#     return list(mongo.db.work.find({"t_id":t_id},{"_id":0}))

# def appointment(t_id,id,start_date,time,item,p_id,done,remark):
#     start_date +="  00:00:00"
#     datetime_object = datetime.strptime(f'{start_date}', '%Y-%m-%d %H:%M:%S')
#     return mongo.db.appointment.insert_one({"t_id":t_id,"id":id,"start_date":datetime_object,"time":time,"item":item,"p_id":p_id,"done":done,"remark":remark})

# def findappointment(p_id):
#     return list(mongo.db.appointment.find({"p_id":p_id},{"_id":0}))