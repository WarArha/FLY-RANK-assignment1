#so the image files that have whole info realated to the execution are stored
#in this lang
from python:3.11-slim

# here workdir acts like cd but difference is that it stays on this app address\
# for the execution of subsequent tasks as well
# the app file provides isolated working environment 
workdir /app

#so copy requirements.txt from my local comp and move to the workdir in the 
# container
copy requirements.txt . 
run pip install --no-cache-dir -r requirements.txt

# all the remaining files are sent after doing the required donwloads and stuff
copy . .

# the port the door to be used is told
expose 8000

cmd ["uvicorn","main2:appi","--host","0.0.0.0","--port","8000"]
