"""Filesystem-related utilities"""

from functools import wraps
import os
import json

CACHE_DIRECTORY = 'tmp/'


def cache_json(filename):
    """Caches the JSON-serializable output of the function to a given file

    Args:
        filename (str) The filename (sans directory) to store the output

    Returns: decorator, applicable to a function that produces JSON-serializable output
    """
    def cache_decorator(cacheable_function):
        @wraps(cacheable_function)
        def cache_wrapper(*args, **kwargs):
            path = CACHE_DIRECTORY + filename
            check_create_folder(path)
            if os.path.exists(path):
                with open(path) as infile:
                    return json.load(infile)
            else:
                function_output = cacheable_function(*args, **kwargs)
                with open(path, 'w') as outfile:
                    json.dump(function_output, outfile)
                return function_output
        return cache_wrapper
    return cache_decorator


def check_create_folder(filename):
    """Check if the folder exisits. If not, create the folder"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
