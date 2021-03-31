from fastapi import FastAPI, File, UploadFile, Depends, Form
import pydantic
from pydantic import BaseModel, Field, BaseConfig
from database import engine, SessionLocal
from models import Song, Podcast, Audiobook
from sqlalchemy.orm import Session
import librosa
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from sqlalchemy import Column, Integer, String, VARCHAR, DateTime, Boolean, LargeBinary
from typing import List,Optional
from database import Base
import json


#creating app
app = FastAPI()



# creating engine
Base.metadata.create_all(engine)



# database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#creating api

@app.post("/upload_song/")
async def create_Song(
    file: UploadFile = File(...), 
    db : Session=Depends(get_db)):

    create_dict = {}
    create_dict["Name"] = file.filename
    create_dict["Uploaded_time"] = datetime.now()
    create_dict["Duration"] = librosa.get_duration(filename= create_dict['Name'])
    song = Song(**create_dict)
    db.add(song)
    db.commit()
    db.refresh(song)
    return song


@app.get('/get/song/')
def get_files(id: int, db: Session = Depends(get_db)):
    try:
        if db.query(Song).filter(Song.ID == id):
            return db.query(Song).filter(Song.ID == id).all()
    except:
        JSONResponse(status_code = 404, content = {"message": "The request is invalid"})


# @app.put('/update_song/{id}')
# async def update_file(id: int, db: Session = Depends(get_db)):
#     try:
#         file = db.query(Song).filter(Song.ID == id).first()
#         update_item_encoded = jsonable_encoder(file)
#         print(update_item)
#         for field in update_item_encoded:
#             if field in update_item and update_item[field] != 0:
#                 setattr(file, field, update_item[field])
#         db.commit()
#         db.refresh(file)
#         return file
#     except:
#         return JSONResponse(status_code = 404, content = {"message": "The request is invalid"})

@app.put("/update_song/{id}")
async def update_item(id: str,
    file: UploadFile = File(...),
    db:Session = Depends(get_db)):

   song = db.query(Song).filter(Song.ID == id).first()
   json_song = jsonable_encoder(song)
   create_Song = {}

   create_Song["Name"]= file.filename
   create_Song["Duration"] = librosa.get_duration(filename= file.filename)
   create_Song["Uploaded_time"] = datetime.now()

   
   update_data = create_Song

   for field in json_song:
       if field in update_data and update_data[field] != 0:
           setattr(song,field,update_data[field])
#    db.add(song)
   db.commit()
   db.refresh(song)
   return song


@app.delete('/delete_Song/{id}/')
def delete_song(id: int, db: Session = Depends(get_db)):
    try:
        db_song = db.query(Song).filter(Song.ID == id).first()
        db.delete(db_song)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Successfully Deleted"})
    except:
        return JSONResponse(status_code = 400, content={"message": "The request is invalid"})



@app.post('/upload_podcast/')
async def podcast(
    podcast_cat : str, 
    host_name: str, 
    participants : List[str] = [],
    file: UploadFile = File(...), 
    
    db: Session = Depends(get_db)):
    
    participant = jsonable_encoder(participants[0])
    create_pod = {}

    create_pod["Name"]= file.filename
    create_pod["Podcast"] = podcast_cat
    create_pod["Duration"] = librosa.get_duration(filename= create_pod['Name'])
    create_pod["Uploaded_time"] = datetime.now()
    create_pod["Host"] = host_name
    create_pod["Participants"] = participant

    podcast = Podcast(**create_pod)
    db.add(podcast)
    db.commit()
    db.refresh(podcast)
    return podcast



@app.get('/get/Podcast/')
def get_files(id: int, db: Session = Depends(get_db)):
    try:
        if db.query(Podcast).filter(Podcast.ID == id):
            return db.query(Podcast).filter(Podcast.ID == id).all()
    except:
        JSONResponse(status_code = 404, content = {"message": "The request is invalid"})


@app.put("/update_podcast/{id}")
async def update_item(
    id:int,
    podcast_cat : str, 
    host_name: str, 
    participants : List[str] = Form(...),
    file: UploadFile = File(...),
    db:Session = Depends(get_db)):


   podc = db.query(Podcast).filter(Podcast.ID == id).first()
   json_podcast = jsonable_encoder(podc)
   create_podcast = {}

   create_podcast["Name"]= file.filename
   create_podcast["Podcast"] = podcast_cat
   create_podcast["Host"] = host_name
   create_podcast["Participants"] = participants
   create_podcast["Duration"] = librosa.get_duration(filename= file.filename)
   create_podcast["Uploaded_time"] = datetime.now()

   
   update_data = create_podcast

   for field in json_podcast:
       if field in update_data and update_data[field] != 0:
           setattr(podc,field,update_data[field])
#    db.add(podc)
   db.commit()
   db.refresh(podc)
   return podc


@app.delete('/delete_Podcast/{id}/')
def delete_Podcast(id: int, db: Session = Depends(get_db)):

    try:
        db_podcast = db.query(Podcast).filter(Podcast.ID == id).first()
        db.delete(db_podcast)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Successfully Deleted"})
    except:
        return JSONResponse(status_code = 400, content={"message": "The request is invalid"})


@app.post('/upload_audiobook/')
async def audiobook(
    Title : str, 
    Author: str, 
    Narrator : str,
    file: UploadFile = File(...), 
    
    db: Session = Depends(get_db)):
    
    create_audiobook = {}

    create_audiobook["Title"]= Title
    create_audiobook["Author"] = Author
    create_audiobook["Duration"] = librosa.get_duration(filename= file.filename)
    create_audiobook["Uploaded_time"] = datetime.now()
    create_audiobook["Narrator"] = Narrator

    audiobook = Audiobook(**create_audiobook)
    db.add(audiobook)
    db.commit()
    db.refresh(audiobook)
    return audiobook


@app.get('/get/audiobook/')
def get_files(id: int, db: Session = Depends(get_db)):
    try:
        if db.query(Audiobook).filter(Audiobook.ID == id):
            return db.query(Audiobook).filter(Audiobook.ID == id).all()
    except:
        JSONResponse(status_code = 404, content = {"message": "The request is invalid"})



@app.put("/update_audiobook/{id}")
async def update_item(id: str, 
    Title : str, 
    Author: str, 
    Narrator : str,
    file: UploadFile = File(...),
    db:Session = Depends(get_db)):

   json_audio = db.query(Audiobook).filter(Audiobook.ID == id).first()
   json_audiobook = jsonable_encoder(json_audio)
   create_audiobook = {}

   create_audiobook["Title"]= Title
   create_audiobook["Author"] = Author
   create_audiobook["Duration"] = librosa.get_duration(filename= file.filename)
   create_audiobook["Uploaded_time"] = datetime.now()
   create_audiobook["Narrator"] = Narrator
   
   update_data = create_audiobook

   for field in json_audiobook:
       if field in update_data and update_data[field] != 0:
           setattr(json_audio,field,update_data[field])
#    db.add(audiobook)
   db.commit()
   db.refresh(json_audio)
   return json_audio


@app.delete('/delete_audiobook/')
def delete_audiobook(id: int, 
    db: Session = Depends(get_db)):
    try:
        db_audiobook = db.query(Audiobook).filter(Audiobook.ID == id).first()
        db.delete(db_audiobook)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Successfully Deleted"})
    except:
        return JSONResponse(status_code = 400, content={"message": "The request is invalid"})


