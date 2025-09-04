'''
Loads YAML config into Python objects.

Validates fields (error thresholds, log paths).
'''
import yaml,logging
from pathlib import Path


# basic setup for logging
logging.basicConfig(filename='./application_logs/config_loader.log',
                    level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
try:
    with open("./config.yaml") as file:
        data = yaml.safe_load(file)
except yaml.YAMLError as e:
    logger.error(f"The yaml is not safe to load, see the error {e} for more information")
except FileNotFoundError:
    logger.error(f"{file} doesn't exists")

# validating services, service, log_path and error threshold
services = data.get('services')
if services is None:
    logger.error("services field doesn't exists")
for service in services:
    service_name = service.get('name')
    log_path = service.get('log_path')
    error_threshold = service.get('error_threshold')
    if service_name is None:
        logger.error(f"service_name is None")
    if type(error_threshold) is not int:
        logger.error(f"error_threshold = {error_threshold} must be an int for {service_name}")
    if log_path is None:
        logger.error(f"log_path is None for {service_name}")
    elif Path(log_path).exists():
        logger.info(f"{log_path} exists,safe to proceed for this {service_name}")
    else:
        logger.error(f"{log_path} doesn't exists, for this service {service_name}")


        

