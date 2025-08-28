'''
Loads config.

Starts asyncio/multiprocessing loops for each service.

Polls log files, parses entries, updates aggregator, triggers alerts, exports metrics.

Handles exceptions gracefully.
'''