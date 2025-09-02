"""
Views - mck Auth App
"""

import json
import sys
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import RedirectView
from django.contrib.auth import logout as auth_logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from config import app_logger
from config import app_seo as seo
from config import settings
from mck_auth import api
from mck_auth import forms
from mck_auth import build_table as bt
from mck_auth import role_validations as rv

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

    @csrf_exempt
    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("landing_page")
        logger.info(request.GET)
        logger.info(request.POST)
        return render(request, self.template_name, context)


class SignIn(TemplateView):
    """
    Admin Login Page
    """
    template_name = "signin.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("signin")
        if request.user.is_authenticated:
            gDict = request.GET
            if 'next' in gDict:
                logger.info(request.user.is_authenticated)
                return HttpResponseRedirect(gDict.get("next"))
            return HttpResponseRedirect(reverse("mck_admin_console:mck_dashboard"))
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        result, message, data = api.user_login(request, for_admin=True)
        logger.info(f"{result} {message} {data}")
        if result:
            gDict = request.GET
            if 'next' in gDict:
                logger.info(request.user.is_authenticated)
                return HttpResponseRedirect(gDict.get("next"))
            return HttpResponseRedirect(reverse("mck_admin_console:mck_dashboard"))
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("signin")
        context['message'] = message
        context['data'] = data
        return render(request, self.template_name, context)


class WebsiteSignIn(TemplateView):
    """
    Website User Login Page
    """
    template_name = "auth/website_signin.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("website_signin")
        if request.user.is_authenticated:
            # Redirect to website home if already logged in
            return HttpResponseRedirect(reverse("mck_website:home_page"))
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        result, message, data = api.user_login(request, for_admin=False)
        logger.info(f"{result} {message} {data}")
        if result:
            return HttpResponseRedirect(reverse("mck_website:home_page"))
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("website_signin")
        context['message'] = message
        context['data'] = data
        return render(request, self.template_name, context)


class WebsiteSignUp(TemplateView):
    """
    Website User Registration Page
    """
    template_name = "auth/website_signup.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("mck_website:home_page"))
        
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("website_signup")
        return render(request, self.template_name, context)

    @csrf_exempt
    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        result, message, data = api.website_user_register(request)
        if result:
            # Auto-login after registration
            login_result, login_message, login_data = api.user_login(request, for_admin=False)
            if login_result:
                return HttpResponseRedirect(reverse("mck_website:home_page"))
        
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("website_signup")
        context['message'] = message
        context['form_data'] = request.POST
        return render(request, self.template_name, context)


class LogOut(RedirectView):
    """
    Admin LogOut Page
    """
    @app_logger.functionlogs(log=LOG_NAME)
    def get_redirect_url(self, **kwargs):
        auth_logout(self.request)
        return reverse("mck_admin_console:mck_landing_page")


class WebsiteLogOut(RedirectView):
    """
    Website User LogOut Page
    """
    @app_logger.functionlogs(log=LOG_NAME)
    def get_redirect_url(self, **kwargs):
        auth_logout(self.request)
        return reverse("mck_website:home_page")
    
# mck_auth/views.py
class WebsitePasswordReset(TemplateView):
    """
    Website User Password Reset
    """
    template_name = "website_password_reset.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("website_password_reset")
        return render(request, self.template_name, context)

    @csrf_exempt
    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        # Implement password reset logic here
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("website_password_reset")
        context['message'] = "Password reset instructions sent to your email."
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class AccountTypeRoleList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs']= seo.get_page_tags("AccountTypeRoleList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission: return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_role_table(request)
        return render(request, self.template_name, context)
    
    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("AccountTypeRoleList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            table_data = bt.build_role_table(request)
            context['table_data'] = table_data
            result, msg, data = api.role_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class AccountTypeRoleCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        try:
            template_name = "role_cu.html"
            context['page_kwargs'] = seo.get_page_tags("AccountTypeRoleList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.AccountTypeRoleCreateUpdateForm()
            context['form'] = form
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, mode=None, *args, **kwargs):
        context = dict()
        try:
            template_name = "role_cu.html"
            context['page_kwargs'] = seo.get_page_tags("AccountTypeRoleList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            form = forms.AccountTypeRoleCreateUpdateForm(request.POST)
            logger.debug(request.POST)
            if form.is_valid():
                result, msg, data = api.role_create_update(request)
                logger.debug(data)
                return HttpResponseRedirect(reverse("mck_auth:mck_role_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class AccountTypeRoleUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            mode = "edit"
            template_name = "role_cu.html"
            context['page_kwargs'] = seo.get_page_tags("AccountTypeRoleList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.role_retrieve_data(request, id)
            form = forms.AccountTypeRoleCreateUpdateForm(instance=data.get("role"), mode=mode)
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
            template_name = "role_cu.html"
            context['page_kwargs'] = seo.get_page_tags("AccountTypeRoleList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg, data = api.role_retrieve_data(request, id)
            form = forms.AccountTypeRoleCreateUpdateForm(request.POST, mode=mode)
            if form.is_valid():
                result, msg, data = api.role_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_auth:mck_role_list"))
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
class AccountTypeRoleDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        try:
            template_name = "role_cu.html"
            context['page_kwargs'] = seo.get_page_tags("AccountTypeRoleList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg = api.role_update_status(request, id)
            return JsonResponse(dict(result=result))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class AccountTypeRoleUpdatePermissionView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id, *args, **kwargs):
        context = dict()
        try:
            template_name = "role_update_permission.html"
            context['page_kwargs'] = seo.get_page_tags("AccountTypeRoleList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg, data = api.role_premission_retrieve_data(request, id)
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id, *args, **kwargs):
        context = dict()
        try:
            template_name = "role_update_permission.html"
            context['page_kwargs'] = seo.get_page_tags("AccountTypeRoleList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission: return render(request, "access_denied.html", context)
            result, msg, data = api.role_update_permission(request, id)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponseRedirect(reverse("mck_auth:mck_role_update_permission", args=[id]))


