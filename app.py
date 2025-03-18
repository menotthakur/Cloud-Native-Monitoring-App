import psutil                                           # this module to get the system metrics
from flask import Flask, render_template                #Application going to run in flash so importe flask

app = Flask(__name__)                                   # create am app which is flask application.

@app.route("/")                                         # set the path where application is going to run. i.e "/" means home path
def index():                                            # define a function index
    cpu_metric = psutil.cpu_percent()                   #hold the value of cpu metric
    mem_metric = psutil.virtual_memory().percent        #hold the value of virutal memory metric in percentage
    Message = None                                      # for now message is defined none
    if cpu_metric > 80 or mem_metric > 80:              
        Message = "High CPU or Memory Detected, scale up!!!"
    return render_template("index.html", cpu_metric=cpu_metric, mem_metric=mem_metric, message=Message) 

if __name__=='__main__':                            # if this file is run as main file then run the application         
    app.run(debug=True, host = '0.0.0.0')           # run the application in debug mode and host is 0.0.0.0 


    # So the flask, and psutil is imported for creating a flask application and getting cpu metrics data.
    