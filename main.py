import os
from fastapi import FastAPI, Request
from typing import Any, List, Dict
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from collections import defaultdict
from dotenv import load_dotenv
load_dotenv()

from crud import checkForValidLogin,createUser,getUserById,createCheckList, getMyList, getListItem, getListName, submitResp, getAllResp, getQuestinDict

templates = Jinja2Templates(directory="templates")

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/login",response_class=HTMLResponse)
async def getLoginFile(request:Request):
    return templates.TemplateResponse("login.html",{"request": request})

@app.get("/register",response_class=HTMLResponse)
async def getRegFile(request:Request):
    return templates.TemplateResponse("register.html",{"request": request})





@app.post("/login")
async def validateLogin(body: Dict[Any, Any]):
    user = checkForValidLogin(body["email"],body["password"])
    if(user == False):
        return {"success":False}
    else:
        return {"success":True,"id":user[0]}
    

@app.post("/register")
async def validateReg(body: Dict[Any, Any]):
    # print(body)
    user = createUser(body["email"],body["password"])
    # print(user)
    if(user == False):
        return {"success":False}
    else:
        return {"success":True,"id":user[0]}

@app.get("/",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse("Home.html",{"request": request})

@app.get("/create-check-list",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse("createCheckList.html",{"request": request})

@app.get("/userdetail/{id}")
async def userDetail(id):
    user = getUserById(id)
    if(not user):
        return {}
    return {"id":user[0],"email":user[1]}

@app.post("/create-check-list")
async def checkList(body: Dict[Any, Any]):
    if createCheckList(body['title'],body['items'],body['id']):
        return {"success":True}
    return {"success":True}

@app.get("/my-check-list/{id}",response_class=HTMLResponse)
async def myList(request:Request,id):
    myList = getMyList(id)
    return templates.TemplateResponse("myList.html",{"myList": myList,"request":request})

@app.get("/checklist/{listid}",response_class=HTMLResponse)
async def fillList(request:Request,listid):
    listItems = getListItem(listid)
    listName = getListName(listid)
    # print(listItems)
    return templates.TemplateResponse("fillList.html",{"request": request,"listName":listName,"listItem":listItems,"listid":listid})

@app.post("/submit/{listid}")
async def submit(body: Dict[Any, Any],listid):
    if body["id"] == None:
        return {"success":False,"msg":"Already submitted"}
    
    res = submitResp(body["id"],listid,body["resp"],body["comment"])
    return {"success":res}

def orderByUser(list):
    # print(list)
    di = defaultdict()
    for item in list:
        if not di.__contains__(str(item[0])):
            di[str(item[0])] = []
        di[str(item[0])].append(item)
    ans = []
    for key in di:
        ans.append(di[key])
    return ans

@app.get("/cheklist-user-response/{listid}/")
async def responseList(request:Request,listid):
    resp = getAllResp(listid)
    listName = getListName(listid)
    listOfList = orderByUser(resp)
    return templates.TemplateResponse("showResp.html",{"request": request,"listOfList":listOfList,"listName":listName,"question":getQuestinDict(listid)})