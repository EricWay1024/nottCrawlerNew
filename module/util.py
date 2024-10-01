import json

def get_mycode(module_obj):
    campus = module_obj["campus"]
    year = module_obj["year"]
    school = module_obj["school"]
    index = module_obj["index"]
    mycode = f"{school}_{index}_{year}_{campus}"
    return mycode

def load_or_fetch(json_path, fetch_func):
    try:
        res = json.load(open(json_path))
    except FileNotFoundError:
        res = fetch_func()
        json.dump(res, open(json_path, "w"))
    return res

def filter_modules(modules_list):
    # Filter out modules from schools named 'United Kingdom' 
    # because they don't contain any useful information and there
    # are hundreds of them
    return [m for m in modules_list if m["school"] != 'UNUK']