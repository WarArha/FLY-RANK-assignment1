from fastapi import FastAPI as appi,  HTTPException,  status
from pydantic import BaseModel as bmw
from typing import Optional as op
import sqlite3 as db

appi=appi()


def get_connection(db_name="tasks.db"):
    conn=db.connect(db_name)
    conn.row_factory=db.Row
    return conn

def create_tables():
    connection=get_connection("tasks.db")
    cursor=connection.cursor()

    cursor.execute("""create table if not exists tasks( 
        id integer primary key AUTOINCREMENT,
        title text not null ,
        done boolean default false)""")

    cursor.execute("select count(*) from tasks")


    if(cursor.fetchone()[0]==0):
        sample_data = [("take bath",False), ("wash cows",True),("feed cows",True) ]

        
        cursor.executemany("insert into tasks(title,done) values (?,?)",sample_data)
        connection.commit()
    connection.close()
        










     

@appi.on_event("startup")
async def start():
    create_tables()






# ------------------------------------ c o d e 

@appi.get("/")
async def status_show():
   return  { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }


@appi.get("/health")
async def h_status():
    return { "status": "ok" }









@appi.get("/tasks")
async def task_list_send():
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("select id,title,done from tasks")
    rows=cursor.fetchall()
    connection.close()
    return [dict(i) for i in rows]# we shall return it as list






@appi.get("/tasks/{id}")
async def one_task_send(id:int):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("select id,title,done from tasks where id = ?",(id,))# we must pass id as tuple
    row=cursor.fetchone()
    connection.close()

    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"task {id} not found")
    return dict(row)




class task_take(bmw):
  
    title:str




@appi.post("/tasks",status_code=201)
async def add_task(task: task_take):
    if task.title.strip()  == "" :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="task title can't be empty")
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("insert into tasks (title,done) values (?,?)",(task.title.strip(),False))
    connection.commit()
    last_id=cursor.lastrowid
    cursor.execute("select * from tasks where id = ?",(last_id,))
    row=cursor.fetchone()
    connection.close()

    return dict(row)
    





class request_body(bmw):
    done_status:op [bool]=None
    title:op [str]=None


@appi.put("/tasks/{id}")
async def update(id:int , request:request_body):


    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("select ")


    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id not found")


@appi.delete("/tasks/{id}",status_code=204)
async def remove(id : int ):

    found = 0

    
    target_index=0
    for i,task in enumerate(in_memory):

        if task["id"]==id:
            in_memory.pop(i)
            found=1
            break
    if found==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id not found")
            
    