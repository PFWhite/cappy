import json
import os
import cappy_config as config

def beautify_json(json_data, sort=True):
    """
    Json should look nice
    """
    return json.dumps(json.loads(json_data), indent=4, sort_keys=sort)

def get_version_files():
    """
    In case you want to see what all the versions are that are supported
    """
    version_path = config.versions_path
    files = os.listdir(version_path)
    return [str(f) for f in files if os.path.isfile(os.path.join(version_path, f)) and ".json" in f]

def path_for_version(filename):
    """
    Function to easily get the path the particular version file
    """
    version_path = config.versions_path
    return os.path.join(version_path, filename)
