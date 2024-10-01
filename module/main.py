from .fetch_brief import get_all_schools, get_all_modules
from .config import SCHOOLS_PATH, MODULE_BRIEF_PATH
from .fetch_modules import run_fetch
from .util import load_or_fetch, filter_modules

if __name__ == '__main__':
    print('Loading or fetching the list of schools...')
    schools = load_or_fetch(SCHOOLS_PATH, get_all_schools)

    print('Loading or fetching the list of all modules...')
    all_modules = load_or_fetch(
        MODULE_BRIEF_PATH, lambda: get_all_modules(schools))
    
    print('Fetching module details...')
    run_fetch(filter_modules(all_modules))