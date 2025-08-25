import sys
from phonenumber_field.phonenumber import PhoneNumber
from django.urls import reverse
from django.forms.models import model_to_dict
from config import app_utils
from config import app_logger
from mck_auth import api as auth_api
from mck_admin_console.models import *


log_name = "app"
logger = app_logger.createLogger(log_name)


@app_logger.functionlogs(log=log_name)
def faq_category_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = FAQCategory.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_admin_console:mck_faq_category_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                    data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a>')
                    # if qs_instance.datamode == "A":
                    #     data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                    #     data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-danger ps-2" onclick="delete_object('+str(qs_data['id'])+')">Inactivate</a></div>')
                    # else:
                    #     data.append('<div class="text-danger">'+qs_instance.get_datamode_display()+'</div>')
                    #     data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-success ps-2" onclick="delete_object('+str(qs_data['id'])+')">Activate</a></div>')
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
def faq_category_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        faq_category = FAQCategory.objects.filter(id=id).first()
        if faq_category:
            data['faq_category'] = faq_category
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def faq_category_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        if mode == 'edit' and id:
            obj = FAQCategory.objects.filter(id=id).first()
        else:
            obj = FAQCategory()
            obj.created_by = accountuser.id
            
        obj.name = pDict.get('name')

        obj.updated_by = accountuser.id
        obj.save()

        data['faq_category'] = obj
        
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def faq_category_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = FAQCategory.objects.filter(id=id).first()
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
def faq_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = FAQ.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_admin_console:mck_faq_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-danger ps-2" onclick="delete_object('+str(qs_data['id'])+')">Inactivate</a></div>')
                    else:
                        data.append('<div class="text-danger">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-success ps-2" onclick="delete_object('+str(qs_data['id'])+')">Activate</a></div>')
                elif column['column_name'] == "faqcategory":
                    data.append(qs_instance.faqcategory.name)
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
def faq_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        faq = FAQ.objects.filter(id=id).first()
        if faq:
            data['faq'] = faq
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def faq_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        if mode == 'edit' and id:
            obj = FAQ.objects.filter(id=id).first()
        else:
            obj = FAQ()
            obj.created_by = accountuser.id
        
        obj.faqcategory = FAQCategory.objects.filter(id=pDict.get('faqcategory')).first()
        obj.question = pDict.get('question')
        obj.answer = pDict.get('answer')
        obj.updated_by = accountuser.id
        obj.save()

        data['faq'] = obj
        
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def faq_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = FAQ.objects.filter(id=id).first()
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
def area_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Area.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_admin_console:mck_area_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-danger ps-2" onclick="delete_object('+str(qs_data['id'])+')">Inactivate</a></div>')
                    else:
                        data.append('<div class="text-danger">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-success ps-2" onclick="delete_object('+str(qs_data['id'])+')">Activate</a></div>')
                elif column['column_name'] == "county":
                    data.append(qs_instance.county.name)
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
def area_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        area = Area.objects.filter(id=id).first()
        if area:
            data['area'] = area
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def area_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        if mode == 'edit' and id:
            obj = Area.objects.filter(id=id).first()
        else:
            obj = Area()
            obj.created_by = accountuser.id
        
        obj.county = County.objects.filter(id=pDict.get('county')).first()
        obj.name = pDict.get('name')
        obj.short_description = pDict.get('short_description')
        obj.address = pDict.get('address')
        obj.tag = pDict.getlist('tag')
        obj.link = pDict.get('link') 

        obj.updated_by = accountuser.id
        obj.save()

        data['area'] = obj
        
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def area_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Area.objects.filter(id=id).first()
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
def testimonial_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Testimonial.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_admin_console:mck_testimonial_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-danger ps-2" onclick="delete_object('+str(qs_data['id'])+')">Inactivate</a></div>')
                    else:
                        data.append('<div class="text-danger">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-success ps-2" onclick="delete_object('+str(qs_data['id'])+')">Activate</a></div>')
                elif column["column_name"] == "photo":
                    if qs_instance.photo:
                        data.append(f'<a href="{qs_instance.photo.url}" target="_blank">View photo</a>')
                    else:
                        data.append("No photo Uploaded")
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
def testimonial_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        testimonial = Testimonial.objects.filter(id=id).first()
        if testimonial:
            data['testimonial'] = testimonial
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def testimonial_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        if mode == 'edit' and id:
            obj = Testimonial.objects.filter(id=id).first()
        else:
            obj = Testimonial()
            obj.created_by = accountuser.id
        
        obj.name = pDict.get('name')
        obj.short_description = pDict.get('short_description')
        obj.description = pDict.get('description')
       
        if 'photo' in request.FILES:
            obj.photo = request.FILES.get('photo')
        elif pDict.get('photo-clear'):
            obj.photo = None
        obj.tags = pDict.get('tags')
        obj.star = pDict.get('star')
        obj.updated_by = accountuser.id
        obj.save()

        data['testimonial'] = obj
        
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def testimonial_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Testimonial.objects.filter(id=id).first()
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

