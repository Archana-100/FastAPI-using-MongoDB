# -*- coding: utf-8 -*-
"""
pip install fastapi, uvicorn

run file python main.py

uvicorn main:app --reload

@author: archa
"""
from fastapi import FastAPI, Query
from pydantic import BaseModel
import uvicorn
from typing import Optional
from bson import ObjectId

import json

app = FastAPI()

#db connection
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

import json
#from flask import jsonify

#client = MongoClient('localhost', 27017, username='username', password='password')

db = client["Gdata"]
gym_collection = db["gymdata2"]


class Person(BaseModel):
    name:str
    address: str
    gender: str
    age: int
    weight: int
  

@app.get('/', status_code=200)
def home():
    return  {"message": "Welcome to Fast API"}

@app.get('/person/{p_id}', status_code=200)
def get_person(p_id: int):
    print(p_id)
    alldata=gym_collection.find({},{"_id":0})
    print(alldata)
    response_msg_list = []
    for msg in alldata:
        response_msg_list.append(Person(**msg))
    return {"data":response_msg_list,"message":"success"}

     
#@app.post('/addPerson/{name}/{address}/{gender}/{age}/{weight}')  
@app.post('/addPerson')    
def add_person(person:Person):
    new_person= {
    "name":person.name,
    "address":person.address,
    "age": person.age,
    "gender": person.gender,
    "weight": person.weight 
    }
    print(new_person)
    # submit_data=gym_collection.insert_one({"name":name,"address":address,"gender":gender,"age":age,
    #                                        "weight":weight})
    submit_data=gym_collection.insert_one(new_person)
    print(submit_data.inserted_id)
    #alldata=list(gym_collection.find({}))
    return {"message":"save data and id "+str(submit_data.inserted_id)}
      
    
 
if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=9090)