'''
Goal:Simulates log entries for multiple services.
    Generates INFO/WARN/ERROR logs with timestamps.
'''
import random
from datetime import datetime,timedelta


# add the service name, datetime in MMDDYYYYHH , count of loglines, step
# NOTE: You can add step in decimel to increment per seconds, default is minutes,
#  Eg: 0.5 step generates in step of 30 seconds
services = [('service1','1109202300',10,0.5), ('service2','1109202300',25,2)]
log_levels = ['INFO','WARN','ERROR']

log_messages = [
        "User login successful",
        "Fetching data from API",
        "Database connection lost",
        "Retrying request",
        "Cache miss",
        "Processed batch job",
        "Disk space low",
        "Request timed out"
]

def generate_log_lines(start_time,count,step):
    log_lines = []
    dt = datetime.strptime(start_time,"%d%m%Y%H%M")
    delta = timedelta(minutes=step)
    for _ in range(count):
        dt += delta
        log_level = random.choice(log_levels)
        message = random.choice(log_messages)
        log_line = f"{datetime.isoformat(dt)} {log_level} {message}"
        log_lines.append(log_line)

    return log_lines

for service in services:
    service_name,start_time,count,step = service
    with open(f"./generated_logs/{service_name}.log",'w') as file:
        generated_lines = generate_log_lines(start_time,count,step)
        for line in generated_lines:
            file.write(line+"\n")

