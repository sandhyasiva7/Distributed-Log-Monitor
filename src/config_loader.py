'''
Loads YAML config into Python objects.

Validates fields (error thresholds, log paths).

Return the services only with valid fields
'''
import yaml,logging
from pathlib import Path
# basic setup for logging
logging.basicConfig(filename='./application_logs/config_loader.log',
                    level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

validation_passed_services = []

def load_and_validate_config(file="./config.yaml"):
    try:
        with open("./config.yaml") as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as e:
        logger.error(f"The yaml is not safe to load, see the error {e} for more information")
        exit
    except FileNotFoundError:
        logger.error(f"{file} doesn't exists")
        exit

    # validating services, service, log_path and error threshold
    services = data.get('services')
    if services is None:
        logger.error("services field doesn't exists")
    for service in services:
        service_name = service.get('name')
        log_path = service.get('log_path')
        error_threshold = service.get('error_threshold')
        valid = True
        if service_name is None:
            logger.error(f"service_name is None")
            valid = False
        if type(error_threshold) is not int:
            logger.error(f"error_threshold = {error_threshold} must be an int for {service_name}")
            valid = False
        if log_path is None:
            logger.error(f"log_path is None for {service_name}")
            valid = False
        if not Path(log_path).exists():
            logger.error(f"{log_path} doesn't exists, for this service {service_name}")
            valid = False
        if valid:
            validation_passed_services.append(service)

    # pass the other configs too
    dedup_configs = data.get('deduplication')

    return validation_passed_services,dedup_configs

# Testing
print(load_and_validate_config("./config.yaml"))


        

