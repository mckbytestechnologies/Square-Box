import os
import datetime
import traceback
import sys
import shutil
import json
import glob
import ast
import traceback
from django.core.management import call_command
from config import settings
from config import app_logger


logger = app_logger.createLogger("app_scripts")

@app_logger.functionlogs(log="app_scripts")
def _load_fixture(fixture_name):
    try:
        logger.info(fixture_name)
        call_command('loaddata','%s'%(fixture_name), verbosity=1)
    except Exception as error:
       logger.error(traceback.format_exc())
       raise error


@app_logger.functionlogs(log="app_scripts")
def run_fixtures(app_name):
    try:
        if app_name:
            app_path = "/".join(app_name.split("."))
            json_folder = os.path.join(settings.BASE_DIR, app_path, 'fixtures', 'json')
            for fixture_name in sorted(glob.glob(json_folder+"/"+"*.json")):
                _load_fixture(fixture_name)
        else:
            apps_list = [ app for app in settings.INSTALLED_APPS if app.startswith("mck_")]
            for app_label in apps_list:
                app_path = "/".join(app_label.split("."))
                json_folder = os.path.join(settings.BASE_DIR, app_path, 'fixtures', 'json')
                for fixture_name in sorted(glob.glob(json_folder+"/"+"*.json")):
                    _load_fixture(fixture_name)
    except Exception as error:
       logger.error(traceback.format_exc())
       raise error

@app_logger.functionlogs(log="app_scripts")
def run():
    logger.info("Starting ...")
    run_fixtures(app_name=None)
    logger.info("End !!!")
