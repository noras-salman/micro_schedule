import micro_schedule
import json
import os 

tasks=json.loads(open('config').read())

micro_schedule.load_tasks(tasks)

micro_schedule.set_logs_enabled(os.getenv('ENABLE_LOGS',False))

micro_schedule.run()