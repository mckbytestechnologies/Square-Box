import os
import traceback
import shutil
import json
import traceback
import pandas as pd
from django.contrib.contenttypes.models import ContentType
from config import settings
from config import app_logger

log_name = "app_scripts"
logger = app_logger.createLogger(log_name)

@app_logger.functionlogs(log=log_name)
def xlsx_to_json(app_label, app_model_list):
    result = False
    try:
        app_path = "/".join(app_label.split("."))
        fixture_path = os.path.join(settings.BASE_DIR, app_path,'fixtures', 'xlsx',"%s.xlsx"%(app_label.split(".")[-1]))
        
        # json folder remove and create
        if os.path.exists(fixture_path):
            json_folder = os.path.join(settings.BASE_DIR, app_path, 'fixtures', 'json')
            if os.path.isdir(json_folder):
                shutil.rmtree(json_folder)
            os.makedirs(json_folder)
            xl = pd.ExcelFile(fixture_path)
            for sheet_count,sheet_name in enumerate(xl.sheet_names):
                if sheet_name.lower() in app_model_list:
                    if len(str(sheet_count)) == 1:
                        sheet_count = "0%s"%(sheet_count)
                    data = xl.parse(sheet_name)

                    json_path = os.path.join(json_folder,"%s-%s-%s.json"%(app_label.split(".")[-1],sheet_count,sheet_name.lower()))
                    count = 0
                    json_list = list()
                    for record in json.loads(data.to_json(orient="records")):
                        for key,value in record.items():
                            if isinstance(value, type(None)):
                                record[key] = ""
                        count += 1
                        updated_record = dict()
                        updated_record['model'] = "%s.%s"%(app_label.split(".")[-1],sheet_name.lower())
                        updated_record['pk'] = count
                        updated_record['fields'] = record
                        json_list.append(updated_record)

                    # data.to_json(json_path, orient='records', lines=False)
                    full_data = json.dumps(json_list)
                    with open(json_path, 'w') as jsonfile:
                        jsonfile.write(full_data)
                    logger.debug("Appname: %s ModelName: %s Success"%(app_label, sheet_name))
                else:
                    logger.warning("Appname: %s ModelName: %s Failed"%(app_label, sheet_name))
        else:
            logger.warning("fixture_path: %s - Not Found"%(fixture_path))
        result = True
    except Exception as error:
        logger.error(traceback.format_exc())
        raise error
    return result


def json_to_xlsx(json_path):
    result = False
    try:
        if os.path.exists(json_path):
            input_file_json = open(json_path, 'r')
            input_field_read =  input_file_json.read()
            input_field = json.loads(input_field_read)
            field_list =[]
            for field in input_field:
                fields = field['fields']
                field_list.append(fields)
            result = pd.DataFrame(data=field_list)
            return result

    except Exception as error:
       logger.error(traceback.format_exc())
       raise error
    return result

@app_logger.functionlogs(log=log_name)
def build_fixtures(app_name):
    try:
        apps_list = [ app for app in settings.INSTALLED_APPS if app.startswith("mck_")]
        if app_name:
            #build fixtures for a specific app
            app_model_list = [model_obj.model for model_obj in ContentType.objects.filter(app_label=app_name.split(".")[-1])]
            result = xlsx_to_json(app_name, app_model_list)
        else:
            #build fixtures for all apps
            for app_label in apps_list:
                app_model_list = [model_obj.model for model_obj in ContentType.objects.filter(app_label=app_label.split(".")[-1])]
                result = xlsx_to_json(app_label, app_model_list)

        return result
    except Exception as error:
        logger.error(traceback.format_exc())
        raise error

@app_logger.functionlogs(log=log_name)
def run():
    logger.info("Starting ...")
    build_fixtures(app_name=None)
    logger.info("End !!!")
