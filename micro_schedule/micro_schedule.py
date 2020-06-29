import datetime
import time
import threading
import requests

triggred_tasks=0
tasks=[]
is_running=False
logs_enabled=False
accepted_days=[str(i) for i in range(1,32)]+["any"]
accepted_monts=[str(i) for i in range(1,13)]+["any"]
 
 
accepted_keys=["at_weekday","at_hour","at_minute","at_second","at_day","at_month","url"]

validation_values={
    "at_weekday":["any","monday","tuesday","wednsday","thursday","friday","saturday","sunday","weekday","weekend"],
    "at_hour":[str(i) for i in range(24)]+["any"],
    "at_minute":[str(i) for i in range(60)]+["any"],
    "at_second":[str(i) for i in range(60)]+["any"],
    "at_day":[str(i) for i in range(1,32)]+["any"],
    "at_month":[str(i) for i in range(1,13)]+["any"]
}

weekdays={
    "monday":[0],
    "tuesday":[1],
    "wednsday":[2],
    "thursday":[3],
    "friday":[4],
    "saturday":[5],
    "sunday":[6],
    "any":[0,1,2,3,4,5,6],
    "weekday":[0,1,2,3,4],
    "weekend":[5,6]
}

def check_weekday(task_weekday,datetime_object):
    return datetime_object.weekday() in weekdays[task_weekday]

def check_hour(task_hour,datetime_object):
    return task_hour=="any" or str(datetime_object.hour)==task_hour

def check_minute(task_minute,datetime_object):
    return task_minute=="any" or str(datetime_object.minute)==task_minute

def check_second(task_second,datetime_object):
    return task_second=="any" or str(datetime_object.second)==task_second

def check_day(task_day,datetime_object):
    return task_day=="any" or str(datetime_object.day)==task_day

def check_month(task_month,datetime_object):
    return task_month=="any" or str(datetime_object.month)==task_month

def check_task(task,datetime_object):
    trigger=True
    if "at_weekday" in task:
        trigger=trigger and check_weekday(task["at_weekday"],datetime_object)
    if "at_hour" in task:
        trigger=trigger and check_hour(task["at_hour"],datetime_object)
    
    if "at_minute" in task:
        trigger=trigger and check_minute(task["at_minute"],datetime_object)
    
    if "at_second" in task:
        trigger=trigger and check_second(task["at_second"],datetime_object)
    
    if "at_day" in task:
        trigger=trigger and check_day(task["at_day"],datetime_object)

    if "at_month" in task:
        trigger=trigger and check_month(task["at_month"],datetime_object)
 
    return trigger


class HookThread (threading.Thread):
    def __init__(self,id,count, url):
        threading.Thread.__init__(self)
        self.url = url
        self.id = id
        self.count = count

    def run(self):
        
        log(self.id,self.count,"Started...")
        log(self.id,self.count,"Requesting"+" "+self.url)
        datetime_start= datetime.datetime.now()
        r=requests.get(self.url,headers={"User-Agent":"micro_schedule"})
        datetime_end= datetime.datetime.now()
        log(self.id,self.count,"Request ended with status"+" "+str(r.status_code))
        log(self.id,self.count,"Elapsed"+" "+str((datetime_end-datetime_start).total_seconds())+" "+"seconds")
        log(self.id,self.count,"Ended.")
        

def log(id,count,text):
    datetime_ts=datetime.datetime.now()
    log_entry="[*][T"+str(id)+"][E"+str(count)+"]\t"+datetime_ts.strftime("%a %Y-%m-%d %H:%M:%S")+"\t"+text
    print(log_entry, flush=True)
    if logs_enabled:
        log_to_file(log_entry)

def log_to_file(log_entry):
    file=open("logs/micro.log","a")
    file.write(log_entry+"\n")
    file.close()

def trigger_tasks(tasks,datetime_object):
    global triggred_tasks
    index=0
    for task in tasks:        
        if check_task(task,datetime_object):
            triggred_tasks+=1
            thread = HookThread(index,triggred_tasks,task["url"])
            thread.start()
        index+=1

def set_logs_enabled(enable_logs=False):
    global logs_enabled
    logs_enabled=enable_logs

def validate_task(task_list):
    if not isinstance(task_list,list):
        raise Exception("tasks should be a list")
    for task in task_list:
        if not isinstance(task,dict):
            raise Exception("Every task should be an object")
        for key in task:
            if not isinstance(key,str):
                raise Exception("All keys should be strings")
            if key not in accepted_keys:
                raise Exception("Unknown key '"+key+"' should be in "+",".join(accepted_keys))
            if not isinstance(task[key],str):
                raise Exception("All values should be strings")
            if key=="url":
                if not (task[key].startswith("http://") or task[key].startswith("https://")):
                    raise Exception("Unaccepted url "+task[key])
            else:
                if task[key] not in validation_values[key]:
                    raise Exception("Unaccepted value for '"+key+"' should be in "+",".join(validation_values[key]))
     


def load_tasks(task_list):
    global tasks
    tasks=task_list
    validate_task(task_list)
    datetime_object = datetime.datetime.now()
    print("[*]\t\t"+datetime_object.strftime("%a %Y-%m-%d %H:%M:%S")+"\tmicro_scedule tasks loaded ..", flush=True)

def run():
    global is_running
    is_running=True
    datetime_object = datetime.datetime.now()
    print("[*]\t\t"+datetime_object.strftime("%a %Y-%m-%d %H:%M:%S")+"\tmicro_scedule started ..", flush=True)
    if len(tasks)==0:
        print("[*]\t\t"+datetime_object.strftime("%a %Y-%m-%d %H:%M:%S")+"\ttmicro_scedule no tasks found", flush=True)
        stop()
    while True:
        if not is_running:
            break
        datetime_object = datetime.datetime.now()
        trigger_tasks(tasks,datetime_object)
        time.sleep(1)

def stop():
    global is_running
    is_running=False
    datetime_object = datetime.datetime.now()
    print("[*]\t\t"+datetime_object.strftime("%a %Y-%m-%d %H:%M:%S")+"\tmicro_scedule stoped ..", flush=True)