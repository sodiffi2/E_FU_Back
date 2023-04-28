from datetime import datetime,timedelta
import json
from model.util import group
from model.db import mongo

def getProfile(e_id):
    return list(mongo.db.user.find({"id":e_id},{"_id":0}))[0]

def editProfile(e_id,name,sex,birth,phone):
    return mongo.db.user.update_one({"id":e_id},{"$set": { "name":name,"sex":sex,"birth":birth,"phone":phone }})

def getEpeople(e_id):
    p_list = list(mongo.db.appointment.find({"e_id": e_id}, {"_id": 0, "f_id": 1}))
    f_ids = []
    for i in p_list:
        f_ids.append(i["f_id"])
    print(f_ids)
    try:
        return list(
        mongo.db.user.aggregate(
            [
                {
                    "$match": {"id": {"$all": f_ids}},
                },
                {
                    "$lookup": {
                        "from": "patient",
                        "localField": "id",
                        "foreignField": "p_id",
                        "as": "result",
                    },
                },
                {"$unwind": "$result"},
                {
                    "$addFields": {
                        "height": "$result.height",
                        "disease": "$result.disease",
                    }
                },
                {"$unset": ["_id", "result"]},
            ]
        )
    )
    except:
        return "error"

def getAppoint(e_id):
    table=["MON","THE","WED","THU","FRI","SAT","SUN"]
    try:
        data=list(
            mongo.db.appointment.aggregate(
                [
                    {"$match": {"e_id": e_id}},
                    {
                        "$group": {
                            "_id": {"start_date": "$start_date", "time": "$time"},
                            "count": {"$count": {}},
                        }
                    },
                    {"$set": {"id": "$_id"}},{"$unset":"_id"}
                    
                ]
            )
        )   
        # res=[]
        for i in data:
            date=i['id']['start_date']
            time=i['id']['time']

            datetime_object = datetime.strptime(f'{date}', '%Y-%m-%d %H:%M:%S')
            
            datetime_object+= timedelta(days=table.index(time[0:3]))
            i['id']['time']=int(f"0x{time[3]}",16)+7
            i['id']['start_date']=datetime_object
            
        return data
    except:
        return "error"
    

    


def getAppointDetail(e_id, start_date, time):
   try:
        return list(
        mongo.db.appointment.aggregate(
            [
                {
                    "$match": {
                        "e_id": e_id,
                        "time": time,
                        "start_date": {"$eq": datetime.fromisoformat(start_date)},
                    }
                },
                {
                    "$lookup": {
                        "from": "user",
                        "localField": "f_id",
                        "foreignField": "id",
                        "as": "result",
                    },
                },
                {"$unwind": {"path": "$result"}},
                {"$addFields": {"name": "$result.name"}},
                {"$unset": ["result", "_id","e_id","start_date","time"]},
            ]
        )
    )
   except:return "error"
