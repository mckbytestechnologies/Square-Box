import sys
from phonenumber_field.phonenumber import PhoneNumber
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.forms.models import model_to_dict
from config import app_utils
from config import app_logger

from mck_auth.models import *

log_name = "app"
logger = app_logger.createLogger(log_name)


@app_logger.functionlogs(log=log_name)
def get_request_accountuser(request):
    try:
        accountuser = AccountUser.objects.filter(user=request.user, is_current_account=True, datamode='A').first()
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return accountuser


# mck_auth/api.py
@app_logger.functionlogs(log=log_name)
def user_login(request, for_admin=True):
    result = False
    message = 'Internal Server Error'
    data = dict()
    try:
        mobile_user = None
        pDict = request.POST
        
        # Find user by email or username
        if User.objects.filter(email=pDict['email'], is_active=True).exists():
            mobile_user = User.objects.filter(email=pDict['email'], is_active=True).first()
        elif User.objects.filter(username=pDict['email'], is_active=True).exists():
            mobile_user = User.objects.filter(username=pDict['email'], is_active=True).first()
        else:
            message = "Invalid User and Password combination"
            return result, message, data
        
        if not mobile_user:
            message = "Invalid User"
            return result, message, data
        
        # Check if user is staff/admin when for_admin=True
        if for_admin and not mobile_user.is_staff:
            message = "Admin access required. Please use the website login."
            return result, message, data
        
        # Check if user is NOT staff when for_admin=False (website users)
        if not for_admin and mobile_user.is_staff:
            message = "Website users cannot login here. Please use the admin login."
            return result, message, data
        
        user = authenticate(username=mobile_user.username, password=pDict['password'])
        if user is not None:
            login(request, user)
            result = True
            message = 'Success'
            data['user'] = user
        else:
            result = False
            data['user'] = user
            message = 'Invalid Password'
        logger.info(f"request user: {request.user.is_authenticated}")
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('sconsole_user_login Error at %s:%s' %(exc_traceback.tb_lineno,e))

    return result, message, data

# mck_auth/api.py
@app_logger.functionlogs(log=log_name)
def website_user_register(request):
    result = False
    message = 'Internal Server Error'
    data = dict()
    try:
        pDict = request.POST
        
        # Validation checks
        if not pDict.get('email') or not pDict.get('password'):
            message = "Email and password are required"
            return result, message, data
        
        if User.objects.filter(email=pDict['email']).exists():
            message = "Email already registered"
            return result, message, data
        
        if User.objects.filter(username=pDict['email']).exists():
            message = "Username already taken"
            return result, message, data
        
        # Create user (non-staff for website users)
        user = User.objects.create_user(
            username=pDict['email'],
            email=pDict['email'],
            password=pDict['password'],
            first_name=pDict.get('first_name', ''),
            last_name=pDict.get('last_name', ''),
            is_staff=False  # Website users are not staff
        )
        
        result = True
        message = 'Registration successful'
        data['user'] = user
        
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('website_user_register Error at %s:%s' %(exc_traceback.tb_lineno,e))
        message = f'Registration failed: {str(e)}'

    return result, message, data


@app_logger.functionlogs(log=log_name)
def ser_login(request):
    result = False
    message = 'Internal Server Error'
    data = dict()
    try:
        mobile_user = None
        pDict = request.POST
        if User.objects.filter(email=pDict['email'], is_active=True).exists():
            mobile_user = User.objects.filter(email=pDict['email'], is_active=True).first()
        else:
            message = "Invalid User and Password combination"
            return result, message, data
        if not mobile_user:
            message = "Invalid User"
            return result, message, data
        user = authenticate(username=mobile_user.username, password=pDict['password'])
        if user is not None:
            login(request, user)
            result = True
            message = 'Success'
            data['user'] = user
        else:
            result = False
            data['user'] = user
            message = 'Invalid Password'
        logger.info(f"request user: {request.user.is_authenticated}")
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('sconsole_user_login Error at %s:%s' %(exc_traceback.tb_lineno,e))

    return result, message, data


@app_logger.functionlogs(log=log_name)
def role_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = AccountTypeRole.objects.exclude(account_type__code='mck').exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_auth:mck_role_update', args=[qs_data['id']])
            permission_url = reverse('mck_auth:mck_role_update_permission', args=[qs_data['id']])


            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-danger ps-2" onclick="delete_object('+str(qs_data['id'])+')">Inactivate</a></div>')
                    else:
                        data.append('<div class="text-danger">'+qs_instance.get_datamode_display()+'</div>')
                        data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-success ps-2" onclick="delete_object('+str(qs_data['id'])+')">Activate</a></div>')
                else:
                    if column['column_name'] == "permissions":
                        data.append('<div class=""><a href="'+permission_url+'" class="text-primary">Update Permission</a></div>')
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
def role_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        role = AccountTypeRole.objects.exclude(account_type__code='mck').filter(id=id).first()
        if role:
            data['role'] = role
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def role_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = get_request_accountuser(request)
        pDict = request.POST
        if mode == 'edit' and id:
            obj = AccountTypeRole.objects.exclude(account_type__code='mck').filter(id=id, datamode='A').first()
        else:
            obj = AccountTypeRole()
            obj.created_by = accountuser.user
        
        obj.account_type = AccountType.objects.filter(code='BUS').first()
        obj.name = pDict.get('name').upper()
        if pDict.get('is_default') == "on":
            AccountTypeRole.objects.exclude(account_type__code='mck').update(is_default=False)
            obj.is_default = True
        else:
            obj.is_default = False
        obj.updated_by = accountuser.user
        obj.save()

        data['role'] = obj
        
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def role_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = get_request_accountuser(request)
        obj = AccountTypeRole.objects.exclude(account_type__code='mck').filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.user
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
def role_premission_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        role = AccountTypeRole.objects.exclude(account_type__code='mck').filter(id=id).first()
        if role:
            data['role'] = role

            master_permissions = MasterPermission.objects.filter(datamode='A').order_by("id")
            role_permission = dict()

            for mp in master_permissions:

                if mp.app_name not in role_permission:
                    role_permission[mp.app_name] = dict()
                    role_permission[mp.app_name]["name"] = mp.app_name.replace("mck_", "").upper()
                    role_permission[mp.app_name]["module"] = dict()

                if mp.module_name not in role_permission[mp.app_name]["module"]:
                    module_obj = dict()
                    role_permission[mp.app_name]["module"][mp.module_name] = dict()
                    role_permission[mp.app_name]["module"][mp.module_name]["name"] = mp.module_name.upper()
                    role_permission[mp.app_name]["module"][mp.module_name]["function"] = dict()

                if mp.function_name not in role_permission[mp.app_name]["module"][mp.module_name]["function"]:
                    role_permission[mp.app_name]["module"][mp.module_name]["function"][mp.function_name] = dict()

                role_permission[mp.app_name]["module"][mp.module_name]["function"][mp.function_name]["has_permission"] = False
                role_permission[mp.app_name]["module"][mp.module_name]["function"][mp.function_name]["function_id"] = mp.id

                if AccountTypeRolePermission.objects.filter(account_type_role=role, master_permission=mp, datamode='A').exists():
                    role_permission[mp.app_name]["module"][mp.module_name]["function"][mp.function_name]["has_permission"] = True

            data['role_permission'] = role_permission
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def role_update_permission(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        pDict = request.POST
        logger.debug(pDict)
        mp_id_list = pDict.getlist("selected_id")
        role = AccountTypeRole.objects.filter(id=id).first()
        if role:
            data['role'] = role
            AccountTypeRolePermission.objects.filter(account_type_role=role).delete()

            for mp_id in mp_id_list:
                at_rp = AccountTypeRolePermission()
                at_rp.account_type_role = role
                at_rp.master_permission = MasterPermission.objects.filter(id=mp_id, datamode='A').first()
                at_rp.has_permission = True
                at_rp.created_by = request.user
                at_rp.updated_by = request.user
                at_rp.save()

            result, msg = True, success_msg
        else:
            result, msg, data = False, error_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

