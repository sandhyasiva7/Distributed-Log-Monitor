'''
part 1:
Reads logs line by line.
Parses timestamps, severity, service name, message and convert raw loglines 
to structured data
part 2:
Deduplicates repeated errors within a time window.
(ignore repeated ERRORs within X seconds)
'''

from config_loader import load_and_validate_config
from datetime import datetime,timedelta

def parse_logs():
    validated_services,dedup_configs ,_= load_and_validate_config()
    hash_to_timestamp_map = {}
    structured_line = {}
    structured_deduped_log = []

    for service in validated_services:
        with open(service['log_path']) as log_file:
            for line in log_file:
                timestamp,severity,message = line.split(" ",2)
                iso_timestamp = datetime.fromisoformat(timestamp)
                message_hash = hash(message)
                should_keep = False         
                if message_hash not in hash_to_timestamp_map:
                    should_keep = True
                elif (iso_timestamp - hash_to_timestamp_map[message_hash]) > timedelta(seconds=dedup_configs['window_seconds']):
                        should_keep = True
                if should_keep:
                    structured_line = {'timestamp': timestamp, 'service':service['name'],
                                'severity': severity,'message': message }
                    structured_deduped_log.append(structured_line)
                hash_to_timestamp_map[message_hash] = iso_timestamp
    return structured_deduped_log

#testing
#print(parse_logs())
