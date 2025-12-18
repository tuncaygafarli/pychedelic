import yaml
import os
from colorama import Fore, Style, Back, init

from utils.console_logger import ConsoleLogger

CONFIG_FILE = "config.yaml"

logger = ConsoleLogger()
init(autoreset=True)

class Configure():
    def __init__(self):
        pass

    def init(self):
        default_config = {
        'assets': {
            'assets_videos': 'assets/videos/',
            'assets_audios': 'assets/audios/',
            'build_dir': 'build',
            'webcam' : 0,
            'use_gpu' : False
        }
    }
        try:
            with open(CONFIG_FILE, 'w') as file:
                yaml.dump(default_config, file, default_flow_style=False, sort_keys=False)
                
            logger.success(f"✅ Successfully created default configuration file: '{CONFIG_FILE}'.")
            return default_config
        
        except IOError as e:
            logger.error(f"An error occurred while writing the file: {e}")
            
        except yaml.YAMLError as e:
            logger.error(f"YAML processing error: {e}")

    def load_config(self):
        try :
            with open(CONFIG_FILE, 'r') as f:
                return yaml.safe_load(f)
            
        except FileNotFoundError:
            logger.error(f"Configuration file '{CONFIG_FILE}' not found. Running " + Fore.GREEN + "python cli.py --init " + Fore.RED + "to initialize configuration.")
            return self.init()
        
        except yaml.YAMLError as e:
            logger.error(f"Configuration file is corrupted (YAML Error: {e}).")
            return None
        
        except Exception as e:
            logger.error(f"Failed to load config file due to an unknown error: {e}")
            return None
        
    def save_config(self, config_data):
        if not os.path.exists(CONFIG_FILE):
            logger.error("Failed to save config file, please run" + Fore.GREEN + "python cli.py --init")
        
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)