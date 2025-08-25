#python LIB
import sys
from django.core.paginator import Paginator

#rest_framework LIB
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response

#project LIB
from config import app_logger
from config import settings

#logger
logger_name = "app"
logger = app_logger.createLogger(logger_name)


HTTP_REST_MESSAGES = {"200": _("Success"),
                      "400": _("Failed"),
                      "401": _("Authentication Failed"),
                      "426": _("Version Mismatch"),
                      "429": _("Too many requests"),
                      "500": _("Internal server error")}


@app_logger.functionlogs(log=logger_name)
def build_response(request, status, message, data=dict(), errors=dict()):
    try:
        # gDict = request.GET.copy()
        # version = gDict.get("ver")
        # app_name = gDict.get("source")
        # is_invalid_version = True
        # app = None
        # if app_name == 'Android_Customer_Mobile_Application':
        #     app = 'CUS_ANDROID_APP'
        # elif app_name == 'iOS_Customer_Mobile_Application':
        #     app = 'CUS_IOS_APP'

        # if request.META.get('HTTP_REFERER') and '/swagger/' in request.META['HTTP_REFERER'] and settings.ENVIRONMENT in ["DEV", "TST"]:
        #     pass
        # else:
        #     if version and app_name and master_model.VersionControl.objects.filter(version=version, app=app, datamode='A').exists():
        #         is_invalid_version = False
        #     if '/api/autogenerate-eod/' in request.path:
        #         is_invalid_version = False
        #     if is_invalid_version:
        #         data = dict()
        #         status = 426
        #         message = HTTP_REST_MESSAGES['426']
        #         data['can_show_primary_msg'] = True
        #         data['can_show_secondary_msg'] = True
        #         data['can_show_btn'] = False
        #         data['is_having_action'] = True
        #         data['btn_text'] = _("Update")
        #         data['android_btn_link'] = settings.ANDROID_APP_LINK
        #         data['ios_btn_link'] = settings.IOS_APP_LINK
        #         data['can_show_btn'] = True
        #         if settings.ENVIRONMENT == "PRD":
        #             data['android_btn_link'] = settings.ANDROID_APP_LINK
        #             data['ios_btn_link'] = settings.IOS_APP_LINK
        #         data['primary_msg_text'] = _("App Update")
        #         data['secondary_msg_text'] = _("Your app version is outdated. Please upgrade to latest version")

        return Response({'status_code': status, 'message': message, 'data':data,'errors': errors}, status=status)
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' %(exc_traceback.tb_lineno,e))


@app_logger.functionlogs(log=logger_name)
def build_webhook_response(request, data, status):
    try:
        return Response(data, status=status)
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' %(exc_traceback.tb_lineno,e))


@app_logger.functionlogs(log="app")
def build_paginated_data(request, queryset, gDict=None):
    try:
        data = dict()
        if not gDict:
            gDict = request.query_params.copy()
        page_number = gDict.get('page_number',1)
        page_size = gDict.get('page_size',10)
        paginator = Paginator(queryset,page_size)
        data['count'] = paginator.count
        data['total_pages'] = paginator.num_pages
        data['per_page'] = 10
        page = paginator.page(page_number)
        data['page_number'] = int(page_number)
        data['previous'] = page.has_previous()
        data['next'] = page.has_next()
        paginated_queryset = page.object_list
        return data, paginated_queryset
    except Exception as e:
        app_logger.exceptionlogs(e)