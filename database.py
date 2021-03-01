import sqlite3
conn=sqlite3.connect("users.db",check_same_thread=False)
c=conn.cursor()
def createdatabase():
    c.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chatid TEXT COLLATE NOCASE
    )
    ''')
    conn.commit()
def lenall():
    c.execute("SELECT * FROM users")
    alluser=c.fetchall()
    return len(alluser)
def getalluser():
    allusers=[]
    c.execute("SELECT chatid FROM users")
    alluser=c.fetchall()
    for i in alluser:
        allusers.append(i[0])
    return allusers
def addchatid(chatid):
    c.execute("SELECT * FROM users WHERE chatid=? LIMIT 1",(chatid,))
    if c.fetchone():
        pass
    else:
        c.execute("INSERT into users values(?,?)",(None,chatid))
        conn.commit()