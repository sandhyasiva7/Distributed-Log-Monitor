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


def main():
    _, _, polling_interval = load_and_validate_config()
    #generates logs for processing 
    log_generator()

    # makes the log lines with structure for all valid services
    # and also applies any deduplication logic
    strucuted_deduped_log = parse_logs()

    aggregate(strucuted_deduped_log,polling_interval)

if __name__ == '__main__':
    main()