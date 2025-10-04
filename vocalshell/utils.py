import json
import logging
def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
def load_config(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return {}
