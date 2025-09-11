'''
Loads config.

Starts asyncio/multiprocessing loops for each service.

Polls log files, parses entries, updates aggregator, triggers alerts, exports metrics.

Handles exceptions gracefully.
'''

from log_generator import log_generator
from log_parser import parse_logs
from aggregator import aggregate
from config_loader import load_and_validate_config
from alert_manager import manage_alert
import json,datetime

def default_serializer(obj):
    if isinstance(obj,datetime.datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    raise TypeError("Type not serliarizable")


def main():
    _, _, polling_interval = load_and_validate_config()
    #generates logs for processing 
    log_generator()

    # makes the log lines with structure for all valid services
    # and also applies any deduplication logic
    strucuted_deduped_log = parse_logs()

    aggregated_metrics = aggregate(strucuted_deduped_log,polling_interval)

    with open("./application_logs/metrics.json", "w") as f:
        json.dump(aggregated_metrics, f, indent=2, default=default_serializer)

    manage_alert(aggregated_metrics)
    
if __name__ == '__main__':
    main()