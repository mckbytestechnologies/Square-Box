import sys
from phonenumber_field.phonenumber import PhoneNumber
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.forms.models import model_to_dict
from config import app_utils
from config import app_logger
from mck_auth.models import *
from mck_auth import api as auth_api
from mck_website.models import *
from squarebox.models import *
from mck_master.models import *
from django.http import JsonResponse
from django.http import HttpResponse
from django.db import transaction
from datetime import datetime


log_name = "app"
logger = app_logger.createLogger(log_name)

# @app_logger.functionlogs(log=log_name)
# def ajax_property_save(request):
#     result = False
#     message = "Failed"

#     try:
#         pDict = request.POST
#         files = request.FILES

#         obj = Property()
#         obj.title = pDict.get("title") or ""
#         obj.description = pDict.get("description") or ""
       
#         obj.city = pDict.get('city') or "" # Fixed: was 'support_description'
#         obj.state = pDict.get('state')or ""
#         obj.zipcode = pDict.get('zipcode')or ""
#         obj.description = pDict.get('description')or ""
#         obj.price = int(pDict.get('price', 0))or ""
#         obj.bedrooms = int(pDict.get('bedrooms', 0))or ""
#         obj.bathrooms = pDict.get('bathrooms') or None
#         obj.sqft = int(pDict.get('sqft', 0))or ""
#         obj.garage = int(pDict.get('garage', 0))or ""
#         obj.created_by = 1
#         obj.updated_by = 1
#         obj.save()

#         # Save ownership
#         own = PropertyType()
#         own.name = pDict.get("name") or ""
#         own.created_by = 1
#         own.updated_by = 1
#         own.save()

#         pho = PropertyImage()
#         pho.property = obj
#         pho.image = files.get("photo")
#         pho.created_by = 1
#         pho.updated_by = 1
#         pho.save()

#         result = True
#         message = "Property Saved Successfully"

#     except Exception as e:
#         exc_type, exc_obj, exc_traceback = sys.exc_info()
#         logger.error("Error at %s:%s" % (exc_traceback.tb_lineno, e))

#     return {
#     "result": result,
#     "message": message
# }

# In your api.py
@app_logger.functionlogs(log=log_name)
def ajax_property_save(request):
    result = False
    message = "Failed to save property"
    
    try:
        logger.info("Processing property save")
        
        # Create Property first
        property_obj = Property(
            title=request.POST.get("title", ""),
            address=request.POST.get("address", ""),
            city=request.POST.get("city", ""),
            state=request.POST.get("state", ""),
            zipcode=request.POST.get("zipcode", ""),
            description=request.POST.get("description", ""),
            price=float(request.POST.get("price", 0)),
            bedrooms=int(request.POST.get("bedrooms", 0)),
            sqft=int(request.POST.get("sqft", 0)),
            garage=int(request.POST.get("garage", 0)),
            created_by=request.user if request.user.is_authenticated else None,
            updated_by=request.user if request.user.is_authenticated else None
        )
        property_obj.save()
        logger.info("Property object created with ID: %s", property_obj.id)
        
        # Handle PropertyType
        property_type_name = request.POST.get("name")
        if property_type_name:
            property_type, created = PropertyType.objects.get_or_create(
                name=property_type_name,
                defaults={
                    'created_by': request.user if request.user.is_authenticated else None,
                    'updated_by': request.user if request.user.is_authenticated else None
                }
            )
            property_obj.property_type = property_type
            property_obj.save()
        
        # Handle Images
        if 'photo' in request.FILES:
            for photo in request.FILES.getlist('photo'):
                PropertyImage.objects.create(
                    property=property_obj,
                    image=photo,
                    created_by=request.user if request.user.is_authenticated else None,
                    updated_by=request.user if request.user.is_authenticated else None
                )
            logger.info("Saved %d photos", len(request.FILES.getlist('photo')))
        
        result = True
        message = "Property saved successfully"
        
    except Exception as e:
        logger.exception("Error in ajax_property_save")
        message = f"Error saving property: {str(e)}"
    
    return result, message



@app_logger.functionlogs(log=log_name)
def ajax_maintenance_save(request):
    result = False
    message = "Failed to save maintenance"
    
    try:
        logger.info("Processing maintenance save")
        
        # Create Property first
        maintenance_obj = MaintenanceRequest(
            description=request.POST.get("description", ""),
            urgency=request.POST.get("urgency", ""),
            preferred_date=request.POST.get("preferred_date", ""),
            attachment=request.POST.get("attachment", ""),
            status=request.POST.get("status", ""),
        
            created_by=request.user if request.user.is_authenticated else None,
            updated_by=request.user if request.user.is_authenticated else None
        )
        maintenance_obj.save()
        logger.info("Maintenace object created with ID: %s", maintenance_obj.id)
        
        result = True
        message = "Property saved successfully"
        
    except Exception as e:
        logger.exception("Error in ajax_property_save")
        message = f"Error saving property: {str(e)}"
    
    return result, message