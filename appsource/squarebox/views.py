import json
import sys
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from config import settings
from mck_auth import build_table as bt
from mck_auth import role_validations as rv
from config import app_logger
from config import app_seo as seo
from squarebox import api
from squarebox import forms
 
LOG_NAME = "app"
logger = app_logger.createLogger(LOG_NAME)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PropertyList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("PropertyList")

        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)

        context['table_data'] = bt.build_property_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = {
            'page_kwargs': seo.get_page_tags("propertyList")
        }

        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)

        try:
            table_data = bt.build_property_table(request)
            context['table_data'] = table_data
            result, msg, data = api.property_load_data(request, table_data)
            return JsonResponse(data, safe=False)
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PropertyCreateView(TemplateView):
    template_name = "common_cu.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = {
            'name': "Property",
            'page_kwargs': seo.get_page_tags("propertyList"),
        }

        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)

        form = forms.PropertyCreateUpdateForm()
        context['form'] = form
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = {
            'name': "Property",
            'page_kwargs': seo.get_page_tags("propertyList"),
        }

        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)

        form = forms.PropertyCreateUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            result, msg, data = api.property_create_update(request)
            return HttpResponseRedirect(reverse("squarebox:property_list"))
        else:
            context['form'] = form
            logger.warning(form.errors)

        return render(request, self.template_name, context)


# @method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
# class PropertyUpdateView(TemplateView):

#     @app_logger.functionlogs(log=LOG_NAME)
#     def get(self, request, id=None, *args, **kwargs):
#         context = dict()
#         try:
#             mode = "edit"
#             template_name = "common_cu.html"
#             context['name'] = "Property"
#             context['page_kwargs'] = seo.get_page_tags("PropertyList")
            
#             has_permission, accountuser = rv.validate_requested_user_function(request)
#             if not has_permission:
#                 return render(request, "access_denied.html", context)

#             context['mode'] = mode
#             result, msg, data = api.property_retrieve_data(request, id)
           
#             form = forms.PropertyCreateUpdateForm(instance=data.get("proeprty"), mode=mode)
#             context['form'] = form
#             context['data'] = data
#         except Exception as e:
#             exc_type, exc_obj, exc_traceback = sys.exc_info()
#             logger.error(f'Error at {exc_traceback.tb_lineno}: {e}')
#             context['error_message'] = "An error occurred while retrieving data."
        
#         return render(request, template_name, context)

#     @app_logger.functionlogs(log=LOG_NAME)
#     def post(self, request, id=None, mode=None, *args, **kwargs):
#         context = dict()
#         try:
#             mode = "edit"
#             template_name = "common_cu.html"
#             context['name'] = "property"
#             context['page_kwargs'] = seo.get_page_tags("PropertyList")
            
#             has_permission, accountuser = rv.validate_requested_user_function(request)
#             if not has_permission:
#                 return render(request, "access_denied.html", context)

#             form = forms.PropertyCreateUpdateForm(request.POST, request.FILES, mode=mode)
#             if form.is_valid():
#                 result, msg, data = api.property_create_update(request, id, mode)
#                 return HttpResponseRedirect(reverse("squarebox:property_list"))
#             else:
#                 logger.warning(form.errors)
#                 context['form'] = form
#                 context['mode'] = mode
#                 context['data'] = data
#         except Exception as e:
#             exc_type, exc_obj, exc_traceback = sys.exc_info()
#             logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
#         return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PropertyUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            mode = "edit"
            template_name = "common_cu.html"
            context['name'] = "Property"
            context['page_kwargs'] = seo.get_page_tags("PropertyList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.property_retrieve_data(request, id)
            form = forms.PropertyCreateUpdateForm(instance=data.get("property"), mode=mode)
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, mode=None, *args, **kwargs):
        context = dict()
        try:
            mode = "edit"
            template_name = "common_cu.html"
            context['name'] = "Property"
            context['page_kwargs'] = seo.get_page_tags("PropertyList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg, data = api.property_retrieve_data(request, id)
            form = forms.PropertyCreateUpdateForm(request.POST, request.FILES, mode=mode)
            if form.is_valid():
                result, msg, data = api.property_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("squarebox:property_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)



@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PropertyDeleteView(TemplateView):
    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = {
            'page_kwargs': seo.get_page_tags("PropertyList")
        }

        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)

        result, msg = api.property_update_status(request, id)
        return JsonResponse({'result': result})


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PropertyTypeList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs']= seo.get_page_tags("PropertyTypeList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission: return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_property_type_table(request)
        return render(request, self.template_name, context)
    
    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("PropertyTypeList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            table_data = bt.build_property_type_table(request)
            context['table_data'] = table_data
            result, msg, data = api.property_type_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PropertyTypeCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            template_name = "common_cu.html"
            context['name'] = "PropertyType"
            context['page_kwargs'] = seo.get_page_tags("PropertyTypeList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.PropertyTypeCreateUpdateForm()
            context['form'] = form
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, mode=None, *args, **kwargs):
        context = dict()
        try:
            template_name = "common_cu.html"
            context['name'] = "PropertyType"
            context['page_kwargs'] = seo.get_page_tags("PropertyTypeList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.PropertyTypeCreateUpdateForm(request.POST, request.FILES)
            logger.debug(request.POST)
            if form.is_valid():
                result, msg, data = api.property_type_create_update(request)
                logger.debug(data)
                return HttpResponseRedirect(reverse("squarebox:property_type_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PropertyTypeUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            mode = "edit"
            template_name = "common_cu.html"
            context['name'] = "PropertyType"
            context['page_kwargs'] = seo.get_page_tags("PropertyTypeList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.property_type_retrieve_data(request, id)
            form = forms.PropertyTypeCreateUpdateForm(instance=data.get("property_type"), mode=mode)
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, mode=None, *args, **kwargs):
        context = dict()
        try:
            mode = "edit"
            template_name = "common_cu.html"
            context['name'] = "PropertyType"
            context['page_kwargs'] = seo.get_page_tags("PropertyTypeList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg, data = api.property_type_retrieve_data(request, id)
            form = forms.PropertyTypeCreateUpdateForm(request.POST, request.FILES, mode=mode)
            if form.is_valid():
                result, msg, data = api.property_type_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("squarebox:property_type_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PropertyTypeDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            template_name = "property_type.html"
            context['page_kwargs'] = seo.get_page_tags("PropertyTypeList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg = api.property_type_update_status(request, id)
            return JsonResponse(dict(result=result))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)




@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class LeadList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs']= seo.get_page_tags("LeadList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission: return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_lead_table(request)
        return render(request, self.template_name, context)
    
    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("LeadList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            table_data = bt.build_lead_table(request)
            context['table_data'] = table_data
            result, msg, data = api.lead_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class LeadCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            template_name = "common_cu.html"
            context['name'] = "Lead"
            context['page_kwargs'] = seo.get_page_tags("LeadList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.LeadCreateUpdateForm()
            context['form'] = form
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, mode=None, *args, **kwargs):
        context = dict()
        try:
            template_name = "common_cu.html"
            context['name'] = "Lead"
            context['page_kwargs'] = seo.get_page_tags("LeadList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.LeadCreateUpdateForm(request.POST, request.FILES)
            logger.debug(request.POST)
            if form.is_valid():
                result, msg, data = api.lead_create_update(request)
                logger.debug(data)
                return HttpResponseRedirect(reverse("squarebox:lead_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class LeadUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            mode = "edit"
            template_name = "common_cu.html"
            context['name'] = "Lead"
            context['page_kwargs'] = seo.get_page_tags("LeadList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.lead_retrieve_data(request, id)
            form = forms.LeadCreateUpdateForm(instance=data.get("lead"), mode=mode)
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, mode=None, *args, **kwargs):
        context = dict()
        try:
            mode = "edit"
            template_name = "common_cu.html"
            context['name'] = "Lead"
            context['page_kwargs'] = seo.get_page_tags("LeadList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg, data = api.lead_retrieve_data(request, id)
            form = forms.LeadCreateUpdateForm(request.POST, request.FILES, mode=mode)
            if form.is_valid():
                result, msg, data = api.lead_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("squarebox:lead_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class LeadDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            template_name = "lead.html"
            context['page_kwargs'] = seo.get_page_tags("LeadList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg = api.lead_update_status(request, id)
            return JsonResponse(dict(result=result))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PropertyImageList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs']= seo.get_page_tags("PropertyTypeList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission: return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_property_image_table(request)
        return render(request, self.template_name, context)
    
    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("PropertyImageList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            table_data = bt.build_property_image_table(request)
            context['table_data'] = table_data
            result, msg, data = api.property_image_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PropertyImageCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            template_name = "common_cu.html"
            context['name'] = "PropertyImage"
            context['page_kwargs'] = seo.get_page_tags("PropertyImageList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.PropertyImageCreateUpdateForm()
            context['form'] = form
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, mode=None, *args, **kwargs):
        context = dict()
        try:
            template_name = "common_cu.html"
            context['name'] = "PropertyImage"
            context['page_kwargs'] = seo.get_page_tags("PropertyImageList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.PropertyImageCreateUpdateForm(request.POST, request.FILES)
            logger.debug(request.POST)
            if form.is_valid():
                result, msg, data = api.property_image_create_update(request)
                logger.debug(data)
                return HttpResponseRedirect(reverse("squarebox:property_image_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PropertyImageUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            mode = "edit"
            template_name = "common_cu.html"
            context['name'] = "PropertyImage"
            context['page_kwargs'] = seo.get_page_tags("PropertyImageList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.property_image_retrieve_data(request, id)
            form = forms.PropertyImageCreateUpdateForm(instance=data.get("property_image"), mode=mode)
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, mode=None, *args, **kwargs):
        context = dict()
        try:
            mode = "edit"
            template_name = "common_cu.html"
            context['name'] = "PropertyImage"
            context['page_kwargs'] = seo.get_page_tags("PropertyImageList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg, data = api.property_image_retrieve_data(request, id)
            form = forms.PropertyImageCreateUpdateForm(request.POST, request.FILES, mode=mode)
            if form.is_valid():
                result, msg, data = api.property_image_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("squarebox:property_image_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PropertyImageDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            template_name = "property_image.html"
            context['page_kwargs'] = seo.get_page_tags("PropertyImageList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg = api.property_image_update_status(request, id)
            return JsonResponse(dict(result=result))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)
    
    #maintaines

    
@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class MaintenanceList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs']= seo.get_page_tags("MaintenanceList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission: return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_maintenance_table(request)
        return render(request, self.template_name, context)
    
    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("MaintenanceList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            table_data = bt.build_maintenance_table(request)
            context['table_data'] = table_data
            result, msg, data = api.maintenance_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class MaintenanceCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            template_name = "common_cu.html"
            context['name'] = "Maintenance"
            context['page_kwargs'] = seo.get_page_tags("MaintenanceList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.MaintenanceCreateUpdateForm()
            context['form'] = form
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, mode=None, *args, **kwargs):
        context = dict()
        try:
            template_name = "common_cu.html"
            context['name'] = "Maintenance"
            context['page_kwargs'] = seo.get_page_tags("MaintenanceList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.MaintenanceCreateUpdateForm(request.POST, request.FILES)
            logger.debug(request.POST)
            if form.is_valid():
                result, msg, data = api.maintenance_create_update(request)
                logger.debug(data)
                return HttpResponseRedirect(reverse("squarebox:maintenance_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class MaintenanceUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            mode = "edit"
            template_name = "common_cu.html"
            context['name'] = "Maintenance"
            context['page_kwargs'] = seo.get_page_tags("MainitenanceList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.maintenance_retrieve_data(request, id)
            form = forms.MaintenanceCreateUpdateForm(instance=data.get("maintenance"), mode=mode)
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, mode=None, *args, **kwargs):
        context = dict()
        try:
            mode = "edit"
            template_name = "common_cu.html"
            context['name'] = "Maintenance"
            context['page_kwargs'] = seo.get_page_tags("MaintenanceList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg, data = api.maintenance_retrieve_data(request, id)
            form = forms.MaintenanceCreateUpdateForm(request.POST, request.FILES, mode=mode)
            if form.is_valid():
                result, msg, data = api.maintenance_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("squarebox:maintenance_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class MaintenanceDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            template_name = "maintenance.html"
            context['page_kwargs'] = seo.get_page_tags("MaintenanceList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg = api.maintenance_update_status(request, id)
            return JsonResponse(dict(result=result))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)