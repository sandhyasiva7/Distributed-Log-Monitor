'''
Maintains rolling counts per service.

Tracks error counts, average logs per interval, etc.
INPUT: Structed_deduped log from log_parser
OUTPUT: For each service print error_counts, total_log_lines / polling window
'''

from datetime import datetime,timedelta

def aggregate(structed_deduped_logs,polling_interval):
    metrics = {}
    for log in structed_deduped_logs:
        service_name = log['service']    
        time_stamp = datetime.fromisoformat(log['timestamp'])
        if service_name not in metrics:
            metrics[service_name] = {
                'intervals' : [],
                'current_interval': {
                    'start_time':  time_stamp,
                    'total_log_lines' : 0,
                    'total_errors': 0
                }
            }
        current_interval = metrics[service_name]['current_interval']
        if (time_stamp - current_interval['start_time'] ) < timedelta(seconds=polling_interval):
            current_interval['total_log_lines'] += 1
            if log['severity'] == 'ERROR':
                current_interval['total_errors'] += 1
        else:
            metrics[service_name]['intervals'].append(current_interval.copy())
            metrics[service_name]['current_interval'] = {
                'start_time': time_stamp,
                'total_log_lines': 1,
                'total_errors': 1 if log['severity'] == 'ERROR' else 0
            }

    for service_name in metrics:
        current_interval = metrics[service_name]['current_interval']
        if current_interval['total_log_lines'] > 0:
            metrics[service_name]['intervals'].append(current_interval.copy())
        # Remove current_interval from final output since it's now in intervals
        del metrics[service_name]['current_interval']
    return metrics


# Unit testing
sample_input = [
                {'timestamp': '2023-09-11T00:00:06', 'service': 'service1', 'severity': 'ERROR', 'message': 'Cache miss\n'}, {'timestamp': '2023-09-11T00:00:12', 'service': 'service1', 'severity': 'INFO', 'message': '®isk space low\n'},
                 {'timestamp': '2023-09-11T00:00:18', 'service': 'service1', 'severity': 'INFO', 'message': 'Request timed out\n'}, {'timestamp': '2023-09-11T00:00:24', 'service': 'service1', 'severity': 'ERROR', 'message': 'Processed batch job\n'}, 
                 {'timestamp': '2023-09-11T00:00:30', 'service': 'service1', 'severity': 'WARN', 'message': 'User login successful\n'},
                   {'timestamp': '2023-09-11T00:00:42', 'service': 'service1', 'severity': 'INFO', 'message': 'Fetching data from API\n'}, {'timestamp': '2023-09-11T00:01:06', 'service': 'service1', 'severity': 'ERROR', 'message': 'Retrying request\n'}, 
                   {'timestamp': '2023-09-11T00:02:18', 'service': 'service1', 'severity': 'ERROR', 'message': 'Database connection lost\n'}, {'timestamp': '2023-09-11T00:03:00', 'service': 'service1', 'severity': 'INFO', 'message': 'User login successful\n'}, 
                   {'timestamp': '2023-09-11T00:04:54', 'service': 'service1', 'severity': 'INFO', 'message': 'Request timed out\n'}, {'timestamp': '2023-09-11T00:06:24', 'service': 'service1', 'severity': 'INFO', 'message': 'Cache miss\n'},
                     {'timestamp': '2023-09-11T00:09:42', 'service': 'service1', 'severity': 'WARN', 'message': 'Request timed out\n'}, {'timestamp': '2023-09-11T00:12:18', 'service': 'service1', 'severity': 'ERROR', 'message': 'Cache miss\n'}, 
                     {'timestamp': '2023-09-11T00:13:18', 'service': 'service1', 'severity': 'INFO', 'message': 'User login successful\n'}, {'timestamp': '2023-09-11T00:13:48', 'service': 'service1', 'severity': 'ERROR', 'message': 'Request timed out\n'}, 
                     {'timestamp': '2023-09-11T00:14:12', 'service': 'service1', 'severity': 'INFO', 'message': 'Fetching data from API\n'}, {'timestamp': '2023-09-11T00:14:24', 'service': 'service1', 'severity': 'ERROR', 'message': 'Disk space low\n'},
                     {'timestamp': '2023-09-11T00:42:36', 'service': 'service2', 'severity': 'INFO', 'message': 'Cache miss\n'}, {'timestamp': '2023-09-11T00:42:48', 'service': 'service2', 'severity': 'ERROR', 'message': 'User login successful\n'}, 
                     {'timestamp': '2023-09-11T00:43:48', 'service': 'service2', 'severity': 'ERROR', 'message': 'Fetching data from API\n'}, {'timestamp': '2023-09-11T00:44:00', 'service': 'service2', 'severity': 'INFO', 'message': 'Retrying request\n'},
                     {'timestamp': '2023-09-11T00:46:12', 'service': 'service2', 'severity': 'ERROR', 'message': 'Processed batch job\n'}, {'timestamp': '2023-09-11T00:46:24', 'service': 'service2', 'severity': 'ERROR', 'message': 'Cache miss\n'},
                    {'timestamp': '2023-09-11T00:47:48', 'service': 'service2', 'severity': 'ERROR', 'message': 'Database connection lost\n'}, {'timestamp': '2023-09-11T00:48:12', 'service': 'service2', 'severity': 'ERROR', 'message': 'User login successful\n'}, 
                       {'timestamp': '2023-09-11T00:48:36', 'service': 'service2', 'severity': 'ERROR', 'message': 'Processed batch job\n'}, {'timestamp': '2023-09-11T00:49:12', 'service': 'service2', 'severity': 'ERROR', 'message': 'Retrying request\n'}, 
                       {'timestamp': '2023-09-11T00:49:48', 'service': 'service2', 'severity': 'ERROR', 'message': 'Fetching data from API\n'}
]

result = aggregate(sample_input,300)
for service, data in result.items():
    print(f"\n{service}:")
    print(f"  Number of intervals: {len(data['intervals'])}")
    for i, interval in enumerate(data['intervals']):
        print(f"  Interval {i+1}: Start={interval['start_time']}, "
              f"Logs={interval['total_log_lines']}, Errors={interval['total_errors']}")