"""
Views - mck Admin Console App
"""
import json
import sys
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from django.contrib.auth import logout as auth_logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from config import app_logger
from config import app_seo as seo
from config import settings
from mck_auth import build_table as bt
from mck_auth import role_validations as rv
from mck_admin_console import api
from mck_admin_console import forms
from django.views.generic.edit import FormView  # Change import if needed
from django.shortcuts import get_object_or_404  # Import this to fetch objects by ID
from mck_admin_console.models import *
from squarebox.models import *
 



LOG_NAME = "app"
logger = app_logger.createLogger(LOG_NAME)


class LandingPage(TemplateView):
    """
    Landing Page
    """
    template_name = "landing_page.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse("mck_admin_console:mck_dashboard"))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class DashboardView(TemplateView):
    """
    Landing Page
    """
    template_name = "dashboard.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("DashboardView")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission: return render(request, "access_denied.html", context)
        context["property"] = Property.objects.exclude(datamode='D').order_by('-updated_on')
        context["property_type"] = PropertyType.objects.exclude(datamode='D').order_by('-updated_on')
        context["property_images"] = PropertyImage.objects.exclude(datamode='D').order_by('-updated_on')
        context["lead"] = Lead.objects.exclude(datamode='D').order_by('-updated_on')
        context["maintenance"] = MaintenanceRequest.objects.exclude(datamode='D').order_by('-updated_on')

        return render(request, self.template_name, context)



@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class FAQCategoryList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs']= seo.get_page_tags("FAQCategoryList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission: return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_faq_category_table(request)
        return render(request, self.template_name, context)
    
    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("FAQCategoryList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            table_data = bt.build_faq_category_table(request)
            context['table_data'] = table_data
            result, msg, data = api.faq_category_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class FAQCategoryCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            template_name = "common_cu.html"
            context['name'] = "FAQCategory"
            context['page_kwargs'] = seo.get_page_tags("FAQCategoryList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.FAQCategoryCreateUpdateForm()
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
            context['name'] = "FAQCategory"
            context['page_kwargs'] = seo.get_page_tags("FAQCategoryList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.FAQCategoryCreateUpdateForm(request.POST, request.FILES)
            logger.debug(request.POST)
            if form.is_valid():
                result, msg, data = api.faq_category_create_update(request)
                logger.debug(data)
                return HttpResponseRedirect(reverse("mck_admin_console:mck_faq_category_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class FAQCategoryUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            mode = "edit"
            template_name = "common_cu.html"
            context['name'] = "FAQCategory"
            context['page_kwargs'] = seo.get_page_tags("FAQCategoryList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.faq_category_retrieve_data(request, id)
            form = forms.FAQCategoryCreateUpdateForm(instance=data.get("faq_category"), mode=mode)
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
            context['name'] = "FAQCategory"
            context['page_kwargs'] = seo.get_page_tags("FAQCategoryList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg, data = api.faq_category_retrieve_data(request, id)
            form = forms.FAQCategoryCreateUpdateForm(request.POST, request.FILES, mode=mode)
            if form.is_valid():
                result, msg, data = api.faq_category_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_admin_console:mck_faq_category_list"))
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
class FAQCategoryDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            template_name = "faq_category.html"
            context['page_kwargs'] = seo.get_page_tags("FAQCategoryList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg = api.faq_category_update_status(request, id)
            return JsonResponse(dict(result=result))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

#faq


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class FAQList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs']= seo.get_page_tags("FAQList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission: return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_faq_table(request)
        return render(request, self.template_name, context)
    
    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("FAQList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            table_data = bt.build_faq_table(request)
            context['table_data'] = table_data
            result, msg, data = api.faq_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class FAQCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            template_name = "common_cu.html"
            context['name'] = "FAQ"
            context['page_kwargs'] = seo.get_page_tags("FAQList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.FAQCreateUpdateForm()
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
            context['name'] = "FAQ"
            context['page_kwargs'] = seo.get_page_tags("FAQList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.FAQCreateUpdateForm(request.POST, request.FILES)
            logger.debug(request.POST)
            if form.is_valid():
                result, msg, data = api.faq_create_update(request)
                logger.debug(data)
                return HttpResponseRedirect(reverse("mck_admin_console:mck_faq_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class FAQUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            mode = "edit"
            template_name = "common_cu.html"
            context['name'] = "FAQ"
            context['page_kwargs'] = seo.get_page_tags("FAQList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.faq_retrieve_data(request, id)
            form = forms.FAQCreateUpdateForm(instance=data.get("faq"), mode=mode)
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
            context['name'] = "FAQ"
            context['page_kwargs'] = seo.get_page_tags("FAQList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg, data = api.faq_retrieve_data(request, id)
            form = forms.FAQCreateUpdateForm(request.POST, request.FILES, mode=mode)
            if form.is_valid():
                result, msg, data = api.faq_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_admin_console:mck_faq_list"))
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
class FAQDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            template_name = "faq.html"
            context['page_kwargs'] = seo.get_page_tags("FAQList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg = api.faq_update_status(request, id)
            return JsonResponse(dict(result=result))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class AreaListView(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("AreaList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission: return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_area_table(request)
        return render(request, self.template_name, context)
    
    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("AreaList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            table_data = bt.build_area_table(request)
            context['table_data'] = table_data
            result, msg, data = api.area_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class AreaCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            template_name = "common_cu.html"
            context['name'] = "Area"
            context['page_kwargs'] = seo.get_page_tags("AreaList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.AreaCreateUpdateForm()
            context['form'] = form
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            template_name = "common_cu.html"
            context['name'] = "Area"
            context['page_kwargs'] = seo.get_page_tags("AreaList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.AreaCreateUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                result, msg, data = api.area_create_update(request)
                return HttpResponseRedirect(reverse("mck_admin_console:mck_area_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class AreaUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            mode = "edit"
            template_name = "common_cu.html"
            context['name'] = "Area"
            context['page_kwargs'] = seo.get_page_tags("AreaList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.area_retrieve_data(request, id)
            form = forms.AreaCreateUpdateForm(instance=data.get("area"), mode=mode)
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
            context['name'] = "Area"
            context['page_kwargs'] = seo.get_page_tags("AreaList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg, data = api.area_retrieve_data(request, id)
            form = forms.AreaCreateUpdateForm(request.POST, request.FILES, mode=mode)
            if form.is_valid():
                result, msg, data = api.area_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_admin_console:mck_area_list"))
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
class AreaDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("AreaList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg = api.area_update_status(request, id)
            return JsonResponse(dict(result=result))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False))


#testimonial


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class TestimonialListView(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("TestimonialList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission: return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_testimonial_table(request)
        return render(request, self.template_name, context)
    
    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("TestimonialList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            table_data = bt.build_testimonial_table(request)
            context['table_data'] = table_data
            result, msg, data = api.testimonial_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class TestimonialCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            template_name = "common_cu.html"
            context['name'] = "Testimonial"
            context['page_kwargs'] = seo.get_page_tags("TestimonialList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.TestimonialCreateUpdateForm()
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
            context['name'] = "Testimonial"
            context['page_kwargs'] = seo.get_page_tags("TestimonialList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.TestimonialCreateUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                result, msg, data = api.testimonial_create_update(request)
                return HttpResponseRedirect(reverse("mck_admin_console:mck_testimonial_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class TestimonialUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            mode = "edit"
            template_name = "common_cu.html"
            context['name'] = "Testimonial"
            context['page_kwargs'] = seo.get_page_tags("TestimonialList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.testimonial_retrieve_data(request, id)
            form = forms.TestimonialCreateUpdateForm(instance=data.get("testimonial"), mode=mode)
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
            context['name'] = "Testimonial"
            context['page_kwargs'] = seo.get_page_tags("TestimonialList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg, data = api.testimonial_retrieve_data(request, id)
            form = forms.TestimonialCreateUpdateForm(request.POST, request.FILES, mode=mode)
            if form.is_valid():
                result, msg, data = api.testimonial_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_admin_console:mck_testimonial_list"))
            else:
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class TestimonialDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            template_name = "testimonial.html"
            context['page_kwargs'] = seo.get_page_tags("TestimonialList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg = api.testimonial_update_status(request, id)
            return JsonResponse(dict(result=result))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)
