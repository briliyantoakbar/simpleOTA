from fastapi import FastAPI, File, UploadFile, HTTPException
import sqlite3
import aiosqlite
import asyncio
import base64
import io
import uuid
from fastapi import Body, FastAPI,UploadFile, File, Request, Form
from fastapi.responses import FileResponse
from secrets import token_hex
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from pydantic import BaseModel
import sqlite3
global versi2
versi2=0
app = FastAPI()
conn=sqlite3.connect("databaseOTA.db",check_same_thread=False)
cursor=conn.cursor()

# Commit the changes and close the connection

# Run the table creation at startup
templates=Jinja2Templates(directory="htmldirectory")

@app.get("/home/", response_class=HTMLResponse)  #Alamat link untuk memasukki menu home
def home(request: Request):
    return templates.TemplateResponse("index.html",{"request":request}) #menampilkan halaman HTML

@app.post("/submitform")
async def index2(versi:int=Form(...),file:UploadFile=File(...)): 
    conn=sqlite3.connect("databaseOTA.db",check_same_thread=False)
    cursor=conn.cursor()
    file_content = await file.read()
    file_name = file.filename
    global versi2
    versi2=versi
    cursor.execute("INSERT INTO ota VALUES (?,?,?,?)",(None,versi,file_name,file_content))
    conn.commit()
    return {"aku":"oke"}

# @app.get("/cat/{versi}") #Alamat link untuk mendownload file
# def catd(versi):
#     global data
#     global datas
#     conn=sqlite3.connect("databaseOTA.db",check_same_thread=False)
#     cursor=conn.cursor()
#     cursor.execute("SELECT id,versi, name,data from ota WHERE versi = ?", (str(versi)))
#     for row in cursor:
#         c=True
#         print("HAIII")
#         print(row[0])
#         print(row[1])
#         print(row[2])
#         data=row[1]
#         datas=row[2]
#     # return {"data":"oke"}
#         return FileResponse(path=datas, media_type="text",filename=data)

@app.get("/c/{versi}")  # Alamat link untuk mendownload file
def catd(versi: str):
    conn = sqlite3.connect("databaseOTA.db", check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("SELECT data FROM ota WHERE versi = ?", (versi,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Version not found")

    image_data = row[0]

    temp_file_path = f"temp_{uuid.uuid4()}.jpg"  # Change extension based on actual image type
    with open(temp_file_path, "wb") as file:
        file.write(image_data)

    response = FileResponse(temp_file_path, media_type='text')

    # Cleanup temporary file after response
    # @response.background
    # def cleanup():
    #     os.remove(temp_file_path)
    return response
    
@app.get("/p/")  #Alamat link untuk request version
def index():
    global versi2
    versi=versi2
    print(versi2)
    return {"version": versi,"url":"https://slope-character-refined-transcription.trycloudflare.com/cat/5"}

