'''
Reads logs line by line.
Parses timestamps, severity, service name, message.
Deduplicates repeated errors within a time window.
'''