#what type of http requests we have 
    # GET, POST, PUT/PATCH, DELETE
# @ is decorator -> adds special functionality in a function 
# async actually gives a function ability to run while some task is in waiting or 
# in some slow working state instead of only waiting in a que



from fastapi import FastAPI as appi,  HTTPException,  status

appi=appi()# its a class so we need a place holder or variable for it 
@appi.get("/")
async def status_show():
   return  { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }


@appi.get("/health")
async def h_status():
    return { "status": "ok" }




#SERVER:- now a server is a building (waits for requests and sends responses)
#DOOR/PORT:- and the doors are enterance in server 
#PATH:- when a request enters a door the path tells what service is exactly desired by that request
#HTTP REQUEST:- protocol://server host:port/path


#FAST API:- it writes logic for how requests are handled (uvicorn directly sends the requests to fastapi)
            #usually used for the backend and 
            #machine learning and ai pipelines(handles asynchronous data transfers extremely fastly)
            
#UVICORN:- is actually the server that listens at door 8000 and sends request to fast api manages the doors and door traffic 
#CURL: so unlike browser which just shows rendered html, json and hides the headers by defualt 
        #this one shows the status + header



#------------------------- stage 2
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


# --------------------------- stage 3
# a data collection class heavily used by fastapi
from pydantic import BaseModel as bmw
class task_take(bmw):
    # this wont work( task_desc="") as pydantic relies on python type annotations :
    title:str




@appi.post("/tasks",status_code=201)
async def add_task(task: task_take):
    if task.title.strip()  == "" :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="task title can't be empty")
    next_id=max((i["id"] for i in in_memory),default=0)+1
    new_task={"id":next_id, "title":task.title.strip(),"done":False}
    in_memory.append(new_task)
    return new_task
# so strip here removes all leading and trailing spaces




#-----------------------------------stage 4
from typing import Optional as op
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
            
    