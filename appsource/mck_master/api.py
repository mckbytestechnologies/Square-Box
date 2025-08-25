import sys
from phonenumber_field.phonenumber import PhoneNumber
from django.urls import reverse
from django.forms.models import model_to_dict
from config import app_utils
from config import app_logger
from mck_auth import api as auth_api
from mck_master.models import *

log_name = "app"
logger = app_logger.createLogger(log_name)


# Support Page Content
@app_logger.functionlogs(log=log_name)
def support_page_content_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = SupportPageContent.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_master:mck_support_page_content_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-danger ps-2" onclick="delete_object('+str(qs_data['id'])+')">Inactivate</a></div>')
                    else:
                        data.append('<div class="text-danger">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-success ps-2" onclick="delete_object('+str(qs_data['id'])+')">Activate</a></div>')
                else:
                    if isinstance(qs_data.get(column['column_name']), PhoneNumber):
                        data.append(qs_data.get(column['column_name']).national_number)
                    elif isinstance(qs_data.get(column['column_name']), models.ImageField):
                        pass
                    else:
                        data.append(qs_data.get(column['column_name'], "-"))
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)

        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def support_page_content_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        support_page_content = SupportPageContent.objects.filter(id=id).first()
        if support_page_content:
            data['support_page_content'] = support_page_content
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def support_page_content_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        if mode == 'edit' and id:
            obj = SupportPageContent.objects.filter(id=id, datamode='A').first()
        else:
            obj = SupportPageContent()
            obj.created_by = accountuser.id
        
        
        obj.support_key = pDict.get('support_key')
        obj.support_value = pDict.get('support_value')
        obj.support_description = pDict.get('support_description')
        obj.image = pDict.get('image')
        obj.content_type = pDict.get('content_type')

        obj.updated_by = accountuser.id
        obj.save()

        data['support_page_content'] = obj
        
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def support_page_content_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = SupportPageContent.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            if obj.datamode == "I":
                obj.datamode = "A"
            else:
                obj.datamode = "I"
            obj.save()

        result = True
        message = 'Sucesss'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# Category
@app_logger.functionlogs(log=log_name)
def category_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Category.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_master:mck_category_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-danger ps-2" onclick="delete_object('+str(qs_data['id'])+')">Inactivate</a></div>')
                    else:
                        data.append('<div class="text-danger">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-success ps-2" onclick="delete_object('+str(qs_data['id'])+')">Activate</a></div>')
                elif column['column_name'] == "name":
                    html_str = ""
                    html_str += '<div class="d-flex align-items-center">';
                    html_str += '<a href="#" class="symbol symbol-50px">';
                    html_str += f'<span class="symbol-label" style="background-image:url({qs_instance.image.url});"></span>';
                    html_str += '</a>';
                    html_str += '<div class="ms-5">';
                    html_str += f'<span class="fw-bold">{qs_instance.name}</span>';
                    html_str += '</div>';
                    html_str += '</div>';
                    data.append(html_str)
                
                else:
                    if isinstance(qs_data.get(column['column_name']), PhoneNumber):
                        data.append(qs_data.get(column['column_name']).national_number)
                    elif isinstance(qs_data.get(column['column_name']), models.ImageField):
                        pass
                    else:
                        data.append(qs_data.get(column['column_name'], "-"))
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)

        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def category_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        category = Category.objects.filter(id=id).first()
        if category:
            data['category'] = category
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def category_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        if mode == 'edit' and id:
            obj = Category.objects.filter(id=id, datamode='A').first()
        else:
            obj = Category()
            obj.created_by = accountuser.id
        
        
        obj.name = pDict.get('name')
        obj.image = pDict.get('image')

        obj.updated_by = accountuser.id
        obj.save()

        data['category'] = obj
        
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def category_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Category.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            if obj.datamode == "I":
                obj.datamode = "A"
            else:
                obj.datamode = "I"
            obj.save()

        result = True
        message = 'Sucesss'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# SubCategory
@app_logger.functionlogs(log=log_name)
def sub_category_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = SubCategory.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_master:mck_sub_category_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-danger ps-2" onclick="delete_object('+str(qs_data['id'])+')">Inactivate</a></div>')
                    else:
                        data.append('<div class="text-danger">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-success ps-2" onclick="delete_object('+str(qs_data['id'])+')">Activate</a></div>')
                elif column['column_name'] == "category":
                    html_str = ""
                    html_str += '<div class="d-flex align-items-center">';
                    html_str += '<a href="#" class="symbol symbol-50px">';
                    html_str += f'<span class="symbol-label" style="background-image:url({qs_instance.category.image.url});"></span>';
                    html_str += '</a>';
                    html_str += '<div class="ms-5">';
                    html_str += f'<span class="fw-bold">{qs_instance.category.name}</span>';
                    html_str += '</div>';
                    html_str += '</div>';
                    data.append(html_str)
                else:
                    if isinstance(qs_data.get(column['column_name']), PhoneNumber):
                        data.append(qs_data.get(column['column_name']).national_number)
                    elif isinstance(qs_data.get(column['column_name']), models.ImageField):
                        pass
                    else:
                        data.append(qs_data.get(column['column_name'], "-"))
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)

        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def sub_category_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        sub_category = SubCategory.objects.filter(id=id).first()
        if sub_category:
            data['sub_category'] = sub_category
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def sub_category_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        if mode == 'edit' and id:
            obj = SubCategory.objects.filter(id=id, datamode='A').first()
        else:
            obj = SubCategory()
            obj.created_by = accountuser.id
        
        obj.category = Category.objects.filter(id=pDict.get('category')).first()
        obj.name = pDict.get('name')
        obj.image = pDict.get('image')
        obj.updated_by = accountuser.id
        obj.save()

        data['sub_category'] = obj
        
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def sub_category_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = SubCategory.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            if obj.datamode == "I":
                obj.datamode = "A"
            else:
                obj.datamode = "I"
            obj.save()

        result = True
        message = 'Sucesss'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


@app_logger.functionlogs(log=log_name)
def ajax_category_based_sub_category(request):
    result = False
    message = 'Error'
    sub_category_list = list()
    try:
        category_id = request.GET.get('category_id')
        sub_category_list = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
        
        result = True
        message = 'Sucesss'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message, sub_category_list


# Banner
@app_logger.functionlogs(log=log_name)
def banner_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Banner.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_master:mck_banner_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-danger ps-2" onclick="delete_object('+str(qs_data['id'])+')">Inactivate</a></div>')
                    else:
                        data.append('<div class="text-danger">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-success ps-2" onclick="delete_object('+str(qs_data['id'])+')">Activate</a></div>')
                else:
                    if isinstance(qs_data.get(column['column_name']), PhoneNumber):
                        data.append(qs_data.get(column['column_name']).national_number)
                    elif isinstance(qs_data.get(column['column_name']), models.ImageField):
                        pass
                    else:
                        data.append(qs_data.get(column['column_name'], "-"))
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)

        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def banner_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        banner = Banner.objects.filter(id=id).first()
        if banner:
            data['banner'] = banner
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def banner_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        if mode == 'edit' and id:
            obj = Banner.objects.filter(id=id, datamode='A').first()
        else:
            obj = Banner()
            obj.created_by = accountuser.id
        
        
        obj.name = pDict.get('name')
        obj.image = pDict.get('image')

        obj.updated_by = accountuser.id
        obj.save()

        data['banner'] = obj
        
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def banner_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Banner.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            if obj.datamode == "I":
                obj.datamode = "A"
            else:
                obj.datamode = "I"
            obj.save()

        result = True
        message = 'Sucesss'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# Gallery
@app_logger.functionlogs(log=log_name)
def gallery_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Gallery.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_master:mck_gallery_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-danger ps-2" onclick="delete_object('+str(qs_data['id'])+')">Inactivate</a></div>')
                    else:
                        data.append('<div class="text-danger">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-success ps-2" onclick="delete_object('+str(qs_data['id'])+')">Activate</a></div>')
                else:
                    if isinstance(qs_data.get(column['column_name']), PhoneNumber):
                        data.append(qs_data.get(column['column_name']).national_number)
                    elif isinstance(qs_data.get(column['column_name']), models.ImageField):
                        pass
                    else:
                        data.append(qs_data.get(column['column_name'], "-"))
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)

        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def gallery_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        gallery = Gallery.objects.filter(id=id).first()
        if gallery:
            data['gallery'] = gallery
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def gallery_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        if mode == 'edit' and id:
            obj = Gallery.objects.filter(id=id, datamode='A').first()
        else:
            obj = Gallery()
            obj.created_by = accountuser.id
        
        
        obj.name = pDict.get('name')
        obj.image = request.FILES.get('image')

        obj.updated_by = accountuser.id
        obj.save()

        data['gallery'] = obj
        
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def gallery_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Gallery.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            if obj.datamode == "I":
                obj.datamode = "A"
            else:
                obj.datamode = "I"
            obj.save()

        result = True
        message = 'Sucesss'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# state
@app_logger.functionlogs(log=log_name)
def state_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = State.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_master:mck_state_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<div class="text-success">' + qs_instance.get_datamode_display() + '</div>')
                        data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-danger ps-2" onclick="delete_object(' + str(qs_data['id']) + ')">Inactivate</a></div>')
                    else:
                        data.append('<div class="text-danger">' + qs_instance.get_datamode_display() + '</div>')
                        data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-success ps-2" onclick="delete_object(' + str(qs_data['id']) + ')">Activate</a></div>')
                elif column['column_name'] == "name":
                    data.append(qs_instance.name)
                elif column['column_name'] == "code":
                    data.append(qs_instance.code)  # Retrieve and display the state code
                elif column['column_name'] == "country":
                    data.append(qs_instance.country.name)  # Assuming `country` is a ForeignKey relation
                else:
                    data.append(qs_data.get(column['column_name'], "-"))
            final_data.append(data)

        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error(f'Error at {exc_traceback.tb_lineno}: {e}')
    
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def state_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        state = State.objects.filter(id=id).first()
        if state:
            data['state'] = state
            data['country'] = state.country 
            result, msg = True, success_msg
        else:
            result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def state_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        
        if mode == 'edit' and id:
            obj = State.objects.filter(id=id).first()
        else:
            obj = State()
            obj.created_by = accountuser.id
        
        obj.name = pDict.get('name')
        obj.code = pDict.get('code')  # Set the code for the state
        obj.country = Country.objects.filter(id=pDict.get('country')).first()  # Assuming country is a ForeignKey
        obj.updated_by = accountuser.id
        obj.save()
        
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error(f'Error at {exc_traceback.tb_lineno}: {e}')
    
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def state_update_status(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = State.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            if obj.datamode == "I":
                obj.datamode = "A"
            else:
                obj.datamode = "I"
            obj.save()
        result = True
        message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    
    return result, message


# city
@app_logger.functionlogs(log=log_name)
def city_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = City.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_master:mck_city_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<div class="text-success">' + qs_instance.get_datamode_display() + '</div>')
                        data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-danger ps-2" onclick="delete_object(' + str(qs_data['id']) + ')">Inactivate</a></div>')
                    else:
                        data.append('<div class="text-danger">' + qs_instance.get_datamode_display() + '</div>')
                        data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-success ps-2" onclick="delete_object(' + str(qs_data['id']) + ')">Activate</a></div>')
                elif column['column_name'] == "name":
                    data.append(qs_instance.name)
                elif column['column_name'] == "state":
                    data.append(qs_instance.state.name)  # Assuming state is a ForeignKey relation
                elif column['column_name'] == "code":
                    data.append(qs_instance.code)  # Retrieve and display the city code
                else:
                    data.append(qs_data.get(column['column_name'], "-"))
            final_data.append(data)

        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error(f'Error at {exc_traceback.tb_lineno}: {e}')
    
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def city_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        city = City.objects.filter(id=id).first()
        if city:
            data['city'] = city
            result, msg = True, success_msg
        else:
            result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def city_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        
        if mode == 'edit' and id:
            obj = City.objects.filter(id=id).first()
        else:
            obj = City()
            obj.created_by = accountuser.id
        
        obj.name = pDict.get('name')
        obj.code = pDict.get('code')  # Set the code for the city
        obj.state = State.objects.filter(id=pDict.get('state')).first()  # Assuming state is a ForeignKey
        obj.updated_by = accountuser.id
        obj.save()
        
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error(f'Error at {exc_traceback.tb_lineno}: {e}')
    
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def city_update_status(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = City.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            if obj.datamode == "I":
                obj.datamode = "A"
            else:
                obj.datamode = "I"
            obj.save()
        result = True
        message = success_msg
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error(f'Error at {exc_traceback.tb_lineno}: {e}')
    
    return result, message

# Offer
@app_logger.functionlogs(log=log_name)
def offer_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Offers.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_master:mck_offer_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-danger ps-2" onclick="delete_object('+str(qs_data['id'])+')">Inactivate</a></div>')
                    else:
                        data.append('<div class="text-danger">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-success ps-2" onclick="delete_object('+str(qs_data['id'])+')">Activate</a></div>')
                else:
                    if isinstance(qs_data.get(column['column_name']), PhoneNumber):
                        data.append(qs_data.get(column['column_name']).national_number)
                    elif isinstance(qs_data.get(column['column_name']), models.ImageField):
                        pass
                    else:
                        data.append(qs_data.get(column['column_name'], "-"))
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)

        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def offer_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        offer = Offers.objects.filter(id=id).first()
        if offer:
            data['offer'] = offer
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def offer_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        if mode == 'edit' and id:
            obj = Offers.objects.filter(id=id, datamode='A').first()
        else:
            obj = Offers()
            obj.created_by = accountuser.id
        
        obj.name = pDict.get('name')
        obj.image = request.FILES.get('image')
        obj.updated_by = accountuser.id
        obj.save()

        data['offer'] = obj
        
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def offer_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Offers.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            if obj.datamode == "I":
                obj.datamode = "A"
            else:
                obj.datamode = "I"
            obj.save()

        result = True
        message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


@app_logger.functionlogs(log=log_name)
def clientfeedback_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = ClientFeedback.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_master:mck_client_feedback_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-danger ps-2" onclick="delete_object('+str(qs_data['id'])+')">Inactivate</a></div>')
                    else:
                        data.append('<div class="text-danger">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-success ps-2" onclick="delete_object('+str(qs_data['id'])+')">Activate</a></div>')
                else:
                    data.append(qs_data.get(column['column_name'], "-"))
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)

        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult

@app_logger.functionlogs(log=log_name)
def clientfeedback_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        clientfeedback = ClientFeedback.objects.filter(id=id).first()
        if clientfeedback:
            data['clientfeedback'] = clientfeedback
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def clientfeedback_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    

    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        if mode == 'edit' and id:
            obj = ClientFeedback.objects.filter(id=id, datamode='A').first()
        else:
            obj = ClientFeedback()
            obj.created_by = accountuser.id
        
        obj.name = pDict.get('name')
        obj.feedback = pDict.get('feedback')
        obj.image = request.FILES.get('image')
        obj.place = pDict.get('place')
        obj.updated_by = accountuser.id
        obj.save()
        data['feedback'] = obj
        
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def clientfeedback_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = ClientFeedback.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            if obj.datamode == "I":
                obj.datamode = "A"
            else:
                obj.datamode = "I"
            obj.save()

        result = True
        message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message
