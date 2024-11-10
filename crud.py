from database import db

def runQuery(q):
    try:
        cursor = db.cursor()
        cursor.execute(q)
        if q.strip().upper().startswith("INSERT") or q.strip().upper().startswith("UPDATE") or q.strip().upper().startswith("DELETE"):
            db.commit()
            rows = cursor.fetchall()
            cursor.close()
            return rows
        elif q.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            cursor.close()
            return rows
        return []
    except Exception as e:
        print("Error executing Query  : "+q)
        print(e)

def createUser(email,password):
    if userExists(email):
        return False
    runQuery(f"INSERT INTO USER(email,password) VALUES('{email}','{password}')")
    rows = runQuery(f"SELECT id FROM USER WHERE EMAIL='{email}'")
    
    if rows == None:
        return False
    
    return rows[0]

def userExists(email):
    rows = runQuery(f"SELECT email FROM USER WHERE email='{email}'")
    # print(rows)
    if(rows==None or len(rows)==0):
        return False
    else:
        return True

def checkForValidLogin(email,password):
    rows = runQuery(f"SELECT id FROM USER WHERE email='{email}' AND password='{password}'")
    # print(rows)
    if(rows==None or len(rows)==0):
        return False
    else:
        return rows[0]

def getUserById(id):
    rows = runQuery(f"SELECT id,email FROM USER WHERE id={id}")
    if(rows==None or len(rows)==0):
        return False
    else:
        return rows[0]
    
def createCheckList(name,items,userid):
    runQuery(f"INSERT INTO CHECKLIST(OWNER_ID,NAME) VALUES({userid},'{name}')")
    # print(runQuery("SELECT * FROM CHECKLIST"))
    listId = runQuery(f"SELECT COUNT(*) FROM CHECKLIST")[0][0]
    # print(items)
    for item in items:
        runQuery(f"INSERT INTO CHECKLISTITEM(LIST_ID,Question) VALUES({listId},'{item}')")
    return True

def getMyList(id):
    # print(runQuery("SELECT * FROM CHECKLISTITEM"))
    rows = runQuery(f"SELECT id, NAME FROM CHECKLIST WHERE OWNER_id={id}")
    return rows

def getListItem(listId):
    items = runQuery(f"SELECT ITEM_ID,Question FROM CHECKLISTITEM WHERE LIST_ID={listId}")
    return items

def getListName(listId):
    row = runQuery(f"SELECT NAME FROM CHECKLIST WHERE id={listId}")
    if(row == None or len(row)==0):
        return False
    return row[0][0]

def submitResp(userid,listid,resp,comment):
    items = getListItem(listId=listid)
    for i in range(len(items)):
        if resp[i] == 'NA':
            r = 'NA'
        elif resp[i] == 'Yes':
            r = 'Yes'
        else:
            r = 'No'
        runQuery(f"INSERT INTO CHECKLISTRESPONSE(USER_ID,ITEM_ID,RES,COMMENT) VALUES({userid},{items[i][0]},'{r}','{comment[i]}')")
    # print(resp)
    # print(comment)
    return True

def getAllResp(listid):
    rows = runQuery(f"SELECT * FROM CHECKLISTRESPONSE WHERE ITEM_ID IN (SELECT ITEM_ID FROM CHECKLISTITEM WHERE LIST_ID={listid})")
    return rows

def getQuestinDict(listid):
    rows = runQuery(f"SELECT * FROM CHECKLISTITEM WHERE LIST_ID={listid}")
    quetions = {}
    for r in rows:
        if(not quetions.__contains__(r[0])):
            quetions[r[0]] = r[2]
    return quetions