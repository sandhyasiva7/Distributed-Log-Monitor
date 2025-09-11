'''
Sends alerts if thresholds exceeded.

Rate-limits alerts per service.

Writes to alerts/alerts.log (optionally prints to console).
'''

from datetime import timedelta 
from config_loader import load_and_validate_config

services,_,_ = load_and_validate_config()

service_alert_configs_map,last_seen = {}, {}
for service in services:
  service_name = service.get('name')
  alert_rate_limit_sec = service.get('alert_rate_limit_sec')
  error_threshold = service.get('error_threshold')
  service_alert_configs_map[service_name] = {"alert_rate_limit": alert_rate_limit_sec,
                                              "error_threshold":error_threshold }

def manage_alert(aggregated_metrics):
    for key in aggregated_metrics:
      item = aggregated_metrics[key]
      if isinstance(item,dict):
         service = key
         intervals = item.get("intervals")
         for interval in intervals:
            total_errors = interval.get("total_errors")
            start_time = interval.get("start_time")
            write_ok = False
            if total_errors > service_alert_configs_map[service]["error_threshold"]:
              if service not in last_seen:
                last_seen[service] = start_time
                write_ok = True
              else:
                 if start_time - last_seen[service] > timedelta(seconds=service_alert_configs_map[service]["alert_rate_limit"]):
                    write_ok = True
                    last_seen[service] = start_time
              if write_ok:
                with open("./alerts/alerts.log",'a') as file:
                  file.write(f"Error threshold exceeded for {service} at {start_time}: {total_errors}\n")

# Unit testing
#manage_alert(./application_logs/metrics.json)