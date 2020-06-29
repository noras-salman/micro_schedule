import micro_schedule
import json
import os 

tasks=json.loads(open('config').read())
micro_schedule.run(tasks,enable_logs=os.getenv('ENABLE_LOGS',False))