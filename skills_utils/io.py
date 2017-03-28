import json
import logging


def stream_json_file(local_file):
    for i, line in enumerate(local_file):
        try:
            data = json.loads(line)
            yield data
        except ValueError as e:
            logging.warning("Skipping line %d due to error: %s", i, e)
            continue
