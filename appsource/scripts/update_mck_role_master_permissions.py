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
def update_role_master_permission():
    try:
        accountuser = AccountUser.objects.filter(account__account_type__code="mck", is_current_account=True, datamode='A').first()
        mp_list = MasterPermission.objects.filter(datamode='A')
        roles = AccountTypeRole.objects.filter(account_type__code="mck", datamode='A')

        for role in roles:
            for mp in mp_list:
                if AccountTypeRolePermission.objects.filter(account_type_role=role, master_permission=mp).exists():
                    at_rp = AccountTypeRolePermission.objects.filter(account_type_role=role, master_permission=mp).first()
                    at_rp.has_permission = True
                    at_rp.created_by = accountuser.user
                    at_rp.save()
                else:
                    at_rp = AccountTypeRolePermission()
                    at_rp.account_type_role = role
                    at_rp.master_permission = mp
                    at_rp.has_permission = True
                    at_rp.created_by = accountuser.user
                    at_rp.updated_by = accountuser.user
                    at_rp.save()

    except Exception as error:
       logger.error(traceback.format_exc())
       raise error

@app_logger.functionlogs(log="app_scripts")
def run():
    logger.info("Starting ...")
    update_role_master_permission()
    logger.info("End !!!")
