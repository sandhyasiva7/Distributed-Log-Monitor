'''
Loads config.

Starts asyncio/multiprocessing loops for each service.

Polls log files, parses entries, updates aggregator, triggers alerts, exports metrics.

Handles exceptions gracefully.
'''

from log_generator import log_generator
from log_parser import parse_logs

def main():
        #generates logs for processing 
    log_generator()

    # makes the log lines with structure for all valid services
    # and also applies any deduplication logic
    strucuted_deduped_log = parse_logs()

    print(strucuted_deduped_log)

if __name__ == '__main__':
    main()