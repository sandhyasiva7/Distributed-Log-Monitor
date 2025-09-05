'''
part 1:
Reads logs line by line.
Parses timestamps, severity, service name, message and convert raw loglines 
to structured data
part 2:
Deduplicates repeated errors within a time window.
'''

from config_loader import load_and_validate_config

def parse_logs():
    validated_services = load_and_validate_config()

    structured_line = {}
    structured_log = []

    for service in validated_services:
        with open(service['log_path']) as log_file:
            for line in log_file:
                timestamp,serverity,message = line.split(" ",2)
                structured_line = {'timestamp': timestamp, 'service':service['name'],
                                'serverity': serverity,'message': message }
                structured_log.append(structured_line)                
    return structured_log

#testing
print(parse_logs())
