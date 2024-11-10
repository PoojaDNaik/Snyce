from database import db


def runQuery(q):
    try:
        cursor = db.cursor()
        cursor.execute(q)
        if q.strip().upper().startswith("INSERT") or q.strip().upper().startswith("UPDATE") or q.strip().upper().startswith("DELETE") or q.strip().upper().startswith("CREATE"):
            db.commit()
            rows = cursor.fetchall()
            cursor.close()
            return rows
        elif q.strip().upper().startswith("SELECT") or q.strip().upper().startswith("DROP"):
            rows = cursor.fetchall()
            cursor.close()
            return rows
        return []
    except Exception as e:
        print("Error executing Query  : "+q)
        print(e)

def f():
    runQuery(
    """
    CREATE TABLE IF NOT EXISTS USER(
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        email varchar(50) UNIQUE,
        password varchar(50) NOT NULL
    )
    """)

    runQuery(
    """
    CREATE TABLE IF NOT EXISTS CHECKLIST(
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        OWNER_id INT,
        NAME varchar(250),
        FOREIGN KEY(OWNER_id) REFERENCES USER(id)
    )
    """
    )

    runQuery(
    """
    CREATE TABLE IF NOT EXISTS CHECKLISTITEM(
        ITEM_ID INT AUTO_INCREMENT PRIMARY KEY,
        LIST_ID INT,
        Question varchar(250),
        FOREIGN KEY(LIST_id) REFERENCES CHECKLIST(id)
    )
    """
    )

    # runQuery("DROP TABLE CHECKLISTRESPONSE")
    runQuery(
    """
    CREATE TABLE IF NOT EXISTS CHECKLISTRESPONSE(
        USER_ID INT,
        ITEM_ID INT,
        RES VARCHAR(50) DEFAULT NULL,
        COMMENT VARCHAR(250) DEFAULT 'NA',
        FOREIGN KEY(ITEM_ID) REFERENCES CHECKLISTITEM(ITEM_ID),
        PRIMARY KEY (USER_ID,ITEM_ID)
    )
    """
    )
    # runQuery("INSERT INTO USER(email,password) VALUES('pavan','123')")
    # print(runQuery("SELECT * FROM USER"))

f()

