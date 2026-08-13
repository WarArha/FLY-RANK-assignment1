from fastapi import FastAPI as appi,  HTTPException,  status
from pydantic import BaseModel as bmw
from typing import Optional as op
import sqlite3 as db

appi=appi()


def get_connection(db_name):
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







in_memory=[{"id":1, "title":"clean house", "done":False},
           {"id":2, "title":"buy groceries", "done":True},
           {"id":3, "title":"wash car", "done":True}
           ]

@appi.get("/tasks")
async def task_list_send():
    return in_memory

@appi.get("/tasks/{id}")
async def one_task_send(id:int):
    for i in in_memory:
        if i["id"]== id:
            return i

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"task {id} not found")





class task_take(bmw):
  
    title:str




@appi.post("/tasks",status_code=201)
async def add_task(task: task_take):
    if task.title.strip()  == "" :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="task title can't be empty")
    next_id=max((i["id"] for i in in_memory),default=0)+1
    new_task={"id":next_id, "title":task.title.strip(),"done":False}
    in_memory.append(new_task)
    return new_task




class request_body(bmw):
    done_status:op [bool]=None
    title:op [str]=None


@appi.put("/tasks/{id}")
async def update(id:int , request:request_body):


    
    for i in in_memory:
        if i["id"]==id:

            if request.title is None and request.done_status is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Must provide title or done_status to update",
                )

            
            if request.title is not None: 
                if request.title.strip() == "":
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="title can't be empty",
                    )
                i["title"]=request.title.strip()
            if request.done_status is not None: 
                i["done"]=request.done_status
            return i

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
            
    