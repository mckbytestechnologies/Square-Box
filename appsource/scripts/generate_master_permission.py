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
from mck_auth.models import *


logger = app_logger.createLogger("app_scripts")


@app_logger.functionlogs(log="app_scripts")
def generate_master_permission():
    try:
        urls = call_command("show_urls", "--format", "pretty-json")
        urls = eval(urls)
        for url in urls:
            if not url['module'].startswith("django") and url['url'].startswith("/mck"):
                url_path = url['module'].split(".")
                full_url = url['url'].split("/")
                module_name = full_url[2]
                function_name = ""
                for index, pattern in enumerate(full_url):
                    if index > 2 and not pattern.startswith("<"):
                        function_name = pattern
                        break

                if MasterPermission.objects.filter(class_name=url_path[-1]).exists():
                    mp = MasterPermission.objects.filter(class_name=url_path[-1]).first()
                else:
                    mp = MasterPermission()
                mp.app_name = url_path[0]
                mp.class_name = url_path[-1]
                mp.module_name = module_name
                mp.function_name = function_name
                mp.datamode = 'A'
                mp.save()

    except Exception as error:
       logger.error(traceback.format_exc())
       raise error

@app_logger.functionlogs(log="app_scripts")
def run():
    logger.info("Starting ...")
    generate_master_permission()
    logger.info("End !!!")
