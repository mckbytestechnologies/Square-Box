import sys
import datetime
from django.urls import reverse
from django.db.models import F
from django.db.models import Sum
from config import app_utils
from config import app_logger
from config import settings
from mck_auth.models import *

log_name = "app"
logger = app_logger.createLogger(log_name)




@app_logger.functionlogs(log=log_name)
def build_role_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "Role"
        table_data['sub_title'] = "Role"
        table_data['load_url'] = reverse('mck_auth:mck_role_list')
        table_data['create_url'] = reverse('mck_auth:mck_role_create')
        table_data['delete_url'] = reverse('mck_auth:mck_role_delete', args=[0])
        table_data["columns"] = list()
        
        table_data["columns"].append(dict(display_name="Name",
                                        can_show=True,
                                        class_name="",
                                        column_name="name",
                                        search_key="name"))

        table_data["columns"].append(dict(display_name="Permissions",
                                        can_show=True,
                                        class_name="",
                                        column_name="permissions",
                                        search_key=""))

        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


@app_logger.functionlogs(log=log_name)
def build_category_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "Category"
        table_data['sub_title'] = "Category"
        table_data['load_url'] = reverse('mck_master:mck_category_list')
        table_data['create_url'] = reverse('mck_master:mck_category_create')
        table_data['delete_url'] = reverse('mck_master:mck_category_delete', args=[0])
        table_data["columns"] = list()
        
        table_data["columns"].append(dict(display_name="Name",
                                        can_show=True,
                                        class_name="",
                                        column_name="name",
                                        search_key="name"))

        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


@app_logger.functionlogs(log=log_name)
def build_banner_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "Banner"
        table_data['sub_title'] = "Banner"
        table_data['load_url'] = reverse('mck_master:mck_banner_list')
        table_data['create_url'] = reverse('mck_master:mck_banner_create')
        table_data['delete_url'] = reverse('mck_master:mck_banner_delete', args=[0])
        table_data["columns"] = list()
        
        table_data["columns"].append(dict(display_name="Name",
                                        can_show=True,
                                        class_name="",
                                        column_name="name",
                                        search_key="name"))

        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data



@app_logger.functionlogs(log=log_name)
def build_gallery_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "Gallery"
        table_data['sub_title'] = "Gallery"
        table_data['load_url'] = reverse('mck_master:mck_gallery_list')
        table_data['create_url'] = reverse('mck_master:mck_gallery_create')
        table_data['delete_url'] = reverse('mck_master:mck_gallery_delete', args=[0])
        table_data["columns"] = list()
        
        table_data["columns"].append(dict(display_name="Name",
                                        can_show=True,
                                        class_name="",
                                        column_name="name",
                                        search_key="name"))

        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


@app_logger.functionlogs(log=log_name)
def build_sub_category_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "SubCategory"
        table_data['sub_title'] = "SubCategory"
        table_data['load_url'] = reverse('mck_master:mck_sub_category_list')
        table_data['create_url'] = reverse('mck_master:mck_sub_category_create')
        table_data['delete_url'] = reverse('mck_master:mck_sub_category_delete', args=[0])
        table_data["columns"] = list()
        
        table_data["columns"].append(dict(display_name="Category",
                                        can_show=True,
                                        class_name="",
                                        column_name="category",
                                        search_key="category"))

        table_data["columns"].append(dict(display_name="Name",
                                        can_show=True,
                                        class_name="",
                                        column_name="name",
                                        search_key="name"))

        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


@app_logger.functionlogs(log=log_name)
def build_support_page_content_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "Support Page Content"
        table_data['sub_title'] = "Support Page Content"
        table_data['load_url'] = reverse('mck_master:mck_support_page_content_list')
        table_data['create_url'] = reverse('mck_master:mck_support_page_content_create')
        table_data['delete_url'] = reverse('mck_master:mck_support_page_content_delete', args=[0])
        table_data["columns"] = list()
        table_data["columns"].append(dict(display_name="Support Key",
                                        can_show=True,
                                        class_name="",
                                        column_name="support_key",
                                        search_key="support_key"))
        table_data["columns"].append(dict(display_name="Support Value",
                                        can_show=True,
                                        class_name="",
                                        column_name="support_value",
                                        search_key="support_value"))
        table_data["columns"].append(dict(display_name="Support Description",
                                        can_show=False,
                                        class_name="",
                                        column_name="support_description",
                                        search_key="support_description"))
        table_data["columns"].append(dict(display_name="Content Type",
                                        can_show=False,
                                        class_name="",
                                        column_name="content_type",
                                        search_key="content_type"))
        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


@app_logger.functionlogs(log=log_name)
def build_enquiry_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "Enquiry"
        table_data['sub_title'] = "Enquiry"
        table_data['load_url'] = reverse('mck_lead_management:mck_enquiry_list')
        table_data['create_url'] = None
        table_data['delete_url'] = reverse('mck_lead_management:mck_enquiry_delete', args=[0])
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="Name",
                                        can_show=True,
                                        class_name="",
                                        column_name="name",
                                        search_key="name"))

        table_data["columns"].append(dict(display_name="Mobile Number",
                                        can_show=True,
                                        class_name="",
                                        column_name="mobile_number",
                                        search_key="mobile_number"))
        
        table_data["columns"].append(dict(display_name="Email",
                                        can_show=True,
                                        class_name="",
                                        column_name="email",
                                        search_key="email"))
        
        table_data["columns"].append(dict(display_name="Permit",
                                        can_show=True,
                                        class_name="",
                                        column_name="permit",
                                        search_key="permit"))
        
        table_data["columns"].append(dict(display_name="Inspection Type",
                                        can_show=True,
                                        class_name="",
                                        column_name="inspection_type",
                                        search_key="inspection_type"))

        table_data["columns"].append(dict(display_name="Address",
                                        can_show=True,
                                        class_name="",
                                        column_name="address",
                                        search_key="address"))
        
        table_data["columns"].append(dict(display_name="Inspection Date",
                                        can_show=True,
                                        class_name="",
                                        column_name="selected_date",
                                        search_key="selected_date"))
        
        table_data["columns"].append(dict(display_name="Inspection Time",
                                        can_show=True,
                                        class_name="",
                                        column_name="selected_time",
                                        search_key="selected_time"))
        
        table_data["columns"].append(dict(display_name="Message",
                                        can_show=True,
                                        class_name="",
                                        column_name="message",
                                        search_key="message"))
        
        table_data["columns"].append(dict(display_name="Enquiry From",
                                        can_show=True,
                                        class_name="",
                                        column_name="enquiry_from",
                                        search_key="enquiry_from"))

        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


@app_logger.functionlogs(log=log_name)
def build_state_table(request):
    table_data = dict()
    try:
        table_data['title'] = "State"
        table_data['sub_title'] = "State Management"
        table_data['load_url'] = reverse('mck_master:mck_state_list')   
        table_data['create_url'] = reverse('mck_master:mck_state_create')  # Adjust URL name as necessary
        table_data['delete_url'] = reverse('mck_master:mck_state_delete', args=[0])  # Adjust URL name as necessary
        table_data["columns"] = list()
        
        table_data["columns"].append(dict(display_name=" name",
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name"))
                                          
        table_data["columns"].append(dict(display_name=" Code",
                                          can_show=True,
                                          class_name="",
                                          column_name="code",
                                          search_key="code"))  # Assuming you have a 'code' field in State model

        table_data["columns"].append(dict(display_name="country",
                                          can_show=True,
                                          class_name="",
                                          column_name="country",
                                          search_key="country"))  # Assuming you have a 'description' field

        table_data["columns"].append(dict(display_name="Status",
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    
    return table_data


@app_logger.functionlogs(log=logger.name)
def build_city_table(request):
    table_data = dict()
    try:
        table_data['title'] = "City"
        table_data['sub_title'] = "City Management"
        table_data['load_url'] = reverse('mck_master:mck_city_list')
        table_data['create_url'] = reverse('mck_master:mck_city_create')
        table_data['delete_url'] = reverse('mck_master:mck_city_delete', args=[0])
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="Name",
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name"))

        table_data["columns"].append(dict(display_name="Code",
                                          can_show=True,
                                          class_name="",
                                          column_name="code",
                                          search_key="code"))

        table_data["columns"].append(dict(display_name="State",
                                          can_show=True,
                                          class_name="",
                                          column_name="state",
                                          search_key="state"))
        
        table_data["columns"].append(dict(display_name="Status",
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))

    return table_data



@app_logger.functionlogs(log=log_name)
def build_offer_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "offer"
        table_data['sub_title'] = "offer"
        table_data['load_url'] = reverse('mck_master:mck_offer_list')
        table_data['create_url'] = reverse('mck_master:mck_offer_create')
        table_data['delete_url'] = reverse('mck_master:mck_offer_delete', args=[0])
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="Name",
                                        can_show=True,
                                        class_name="",
                                        column_name="name",
                                        search_key="name"))

        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


@app_logger.functionlogs(log=log_name)
def build_client_feedback_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "client feedback"
        table_data['sub_title'] = "client feedback"
        table_data['load_url'] = reverse('mck_master:mck_client_feedback_list')  # URL for loading the table data
        table_data['create_url'] = reverse('mck_master:mck_client_feedback_create')  # URL for creating new feedback
        table_data['delete_url'] = reverse('mck_master:mck_client_feedback_delete', args=[0])  # URL for deleting feedback
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name=" Name",  # Name of the client giving feedback
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name"))

        table_data["columns"].append(dict(display_name="Feedback",  # Feedback content
                                          can_show=True,
                                          class_name="",
                                          column_name="feedback",
                                          search_key="feedback"))
        
        table_data["columns"].append(dict(display_name="Place",  # Name of the client giving feedback
                                          can_show=True,
                                          class_name="",
                                          column_name="place",
                                          search_key="place"))

        table_data["columns"].append(dict(display_name="Status",  # Status of the feedback (Active/Inactive)
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data




@app_logger.functionlogs(log=log_name)
def build_faq_category_table(request):
    table_data = dict()
    try:
        table_data['title'] = "FAQCategory"
        table_data['sub_title'] = "FAQCategory Management"
        table_data['load_url'] = reverse('mck_admin_console:mck_faq_category_list')  
        table_data['create_url'] = reverse('mck_admin_console:mck_faq_category_create')  
        table_data['delete_url'] = reverse('mck_admin_console:mck_faq_category_delete', args=[0,])  
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="Name",  
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name"))  

 

        table_data["columns"].append(dict(display_name="Status",  
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data



@app_logger.functionlogs(log=log_name)
def build_faq_table(request):
    table_data = dict()
    try:
        table_data['title'] = "FAQ"
        table_data['sub_title'] = "FAQ Management"
        table_data['load_url'] = reverse('mck_admin_console:mck_faq_list')  
        table_data['create_url'] = reverse('mck_admin_console:mck_faq_create')  
        table_data['delete_url'] = reverse('mck_admin_console:mck_faq_delete', args=[0,])  
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="FAQategory",  
                                          can_show=True,
                                          class_name="",
                                          column_name="faqcategory",
                                          search_key="faqcategory"))  
        
        table_data["columns"].append(dict(display_name="Question",  
                                          can_show=True,
                                          class_name="",
                                          column_name="question",
                                          search_key="question")) 
        
        table_data["columns"].append(dict(display_name="Answer",  
                                          can_show=True,
                                          class_name="",
                                          column_name="answer",
                                          search_key="answer")) 

 

        table_data["columns"].append(dict(display_name="Status",  
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data




@app_logger.functionlogs(log=log_name)
def build_area_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Area"
        table_data['sub_title'] = "Area Management"
        table_data['load_url'] = reverse('mck_admin_console:mck_area_list')  
        table_data['create_url'] = reverse('mck_admin_console:mck_area_create')  
        table_data['delete_url'] = reverse('mck_admin_console:mck_area_delete', args=[0,])  
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="County",  
                                          can_show=True,
                                          class_name="",
                                          column_name="county",
                                          search_key="county"))  
        
        table_data["columns"].append(dict(display_name="Name",  
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name")) 
        
        table_data["columns"].append(dict(display_name="Address",  
                                          can_show=True,
                                          class_name="",
                                          column_name="address",
                                          search_key="address")) 
        
        table_data["columns"].append(dict(display_name="Status",  
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data



@app_logger.functionlogs(log=log_name)
def build_testimonial_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Testimonial"
        table_data['sub_title'] = "Testimonial Management"
        table_data['load_url'] = reverse('mck_admin_console:mck_testimonial_list')  
        table_data['create_url'] = reverse('mck_admin_console:mck_testimonial_create')  
        table_data['delete_url'] = reverse('mck_admin_console:mck_testimonial_delete', args=[0,])  
        table_data["columns"] = list()
  
        
        table_data["columns"].append(dict(display_name="Name",  
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name")) 
        
        table_data["columns"].append(dict(display_name=" Description",  
                                          can_show=True,
                                          class_name="",
                                          column_name="description",
                                          search_key="description")) 
        
        table_data["columns"].append(dict(display_name="Star",  
                                          can_show=True,
                                          class_name="",
                                          column_name="star",
                                          search_key="star")) 

        table_data["columns"].append(dict(display_name="Status",  
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data



@app_logger.functionlogs(log=log_name)
def build_county_table(request):
    table_data = dict()
    try:
        table_data['title'] = "County"
        table_data['sub_title'] = "County Management"
        table_data['load_url'] = reverse('mck_admin_console:mck_county_list')  
        table_data['create_url'] = reverse('mck_admin_console:mck_county_create')  
        table_data['delete_url'] = reverse('mck_admin_console:mck_county_delete', args=[0,])  
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="Name",  
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name"))  

 

        table_data["columns"].append(dict(display_name="Status",  
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


@app_logger.functionlogs(log=log_name)
def build_teams_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Teams"
        table_data['sub_title'] = "Teams Management"
        table_data['load_url'] = reverse('mck_admin_console:mck_team_list')  
        table_data['create_url'] = reverse('mck_admin_console:mck_team_create')  
        table_data['delete_url'] = reverse('mck_admin_console:mck_team_delete', args=[0,])  
        table_data["columns"] = list()
        

        table_data["columns"].append(dict(display_name="Name",  
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name"))
        
        table_data["columns"].append(dict(display_name="designation",  
                                          can_show=True,
                                          class_name="",
                                          column_name="designation",
                                          search_key="designation")) 
         
        table_data["columns"].append(dict(display_name="description",  
                                          can_show=True,
                                          class_name="",
                                          column_name="description",
                                          search_key="description"))  

        table_data["columns"].append(dict(display_name="Status",  
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data




@app_logger.functionlogs(log=log_name)
def build_property_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Property"
        table_data['sub_title'] = "Property Management"
        table_data['load_url'] = reverse('squarebox:property_list')   
        table_data['create_url'] = reverse('squarebox:property_create')  # Adjust URL name as necessary
        table_data['delete_url'] = reverse('squarebox:property_delete', args=[0])  # Adjust URL name as necessary
        table_data["columns"] = list()
        
        table_data["columns"].append(dict(display_name="title",
                                          can_show=True,
                                          class_name="",
                                          column_name="title",
                                          search_key="title"))
                                          
        table_data["columns"].append(dict(display_name="address",
                                          can_show=True,
                                          class_name="",
                                          column_name="address",
                                          search_key="address"))  # Assuming you have a 'code' field in State model

        table_data["columns"].append(dict(display_name="Property Type",
                                          can_show=True,
                                          class_name="",
                                          column_name="property_type",
                                          search_key="property_type"))  # Assuming you have a 'description' field

        table_data["columns"].append(dict(display_name="Status",
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    
    return table_data


@app_logger.functionlogs(log=log_name)
def build_property_type_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Property Type"
        table_data['sub_title'] = "Property Type Management"
        table_data['load_url'] = reverse('squarebox:property_type_list')  
        table_data['create_url'] = reverse('squarebox:property_type_create')  
        table_data['delete_url'] = reverse('squarebox:property_type_delete', args=[0,])  
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="Name",  
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name"))  

 

        table_data["columns"].append(dict(display_name="Status",  
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data




@app_logger.functionlogs(log=log_name)
def build_lead_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Lead"
        table_data['sub_title'] = "Lead Management"
        table_data['load_url'] = reverse('squarebox:lead_list')  
        table_data['create_url'] = reverse('squarebox:lead_create')  
        table_data['delete_url'] = reverse('squarebox:lead_delete', args=[0,])  
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="Name",  
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name")) 

        table_data["columns"].append(dict(display_name="Message",  
                                          can_show=True,
                                          class_name="",
                                          column_name="message",
                                          search_key="message"))  

 

        table_data["columns"].append(dict(display_name="Status",  
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data



@app_logger.functionlogs(log=log_name)
def build_property_image_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Property Image"
        table_data['sub_title'] = "Property Image Management"
        table_data['load_url'] = reverse('squarebox:property_image_list')  
        table_data['create_url'] = reverse('squarebox:property_image_create')  
        table_data['delete_url'] = reverse('squarebox:property_image_delete', args=[0,])  
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="Property",  
                                          can_show=True,
                                          class_name="",
                                          column_name="property",
                                          search_key="proeprty"))  
        
        table_data["columns"].append(dict(display_name="Status",  
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


@app_logger.functionlogs(log=log_name)
def build_maintenance_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Maintenance"
        table_data['sub_title'] = "Maintenance Management"
        table_data['load_url'] = reverse('squarebox:maintenance_list')  
        table_data['create_url'] = reverse('squarebox:maintenance_create')  
        table_data['delete_url'] = reverse('squarebox:maintenance_delete', args=[0,])  
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="description",  
                                          can_show=True,
                                          class_name="",
                                          column_name="description",
                                          search_key="description"))  
        
        table_data["columns"].append(dict(display_name="Status",  
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data

