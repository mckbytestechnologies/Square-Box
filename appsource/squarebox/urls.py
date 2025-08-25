
from django.urls import path
from squarebox import views

app_name = "squarebox"

urlpatterns = [
    path('property/list/', views.PropertyList.as_view(),name='property_list'),
    path('property/create/', views.PropertyCreateView.as_view(),name='property_create'),
    path('property/<id>/edit/', views.PropertyUpdateView.as_view(),name='property_update'),
    path('property/<id>/delete/', views.PropertyDeleteView.as_view(),name='property_delete'),

    path('property-type/list/', views.PropertyTypeList.as_view(),name='property_type_list'),
    path('property-type/create/', views.PropertyTypeCreateView.as_view(),name='property_type_create'),
    path('property-type/<id>/edit/', views.PropertyTypeUpdateView.as_view(),name='property_type_update'),
    path('property-type/<id>/delete/', views.PropertyTypeDeleteView.as_view(),name='property_type_delete'),
    
    path('lead/list/', views.LeadList.as_view(),name='lead_list'),
    path('lead/create/', views.LeadCreateView.as_view(),name='lead_create'),
    path('lead/<id>/edit/', views.LeadUpdateView.as_view(),name='lead_update'),
    path('lead/<id>/delete/', views.LeadDeleteView.as_view(),name='lead_delete'),

    path('property-image/list/', views.PropertyImageList.as_view(),name='property_image_list'),
    path('property-image/create/', views.PropertyImageCreateView.as_view(),name='property_image_create'),
    path('property-image/<id>/edit/', views.PropertyImageUpdateView.as_view(),name='property_image_update'),
    path('property-image/<id>/delete/', views.PropertyImageDeleteView.as_view(),name='property_image_delete'),

    path('maintenance/list/', views.MaintenanceList.as_view(),name='maintenance_list'),
    path('maintenance/create/', views.MaintenanceCreateView.as_view(),name='maintenance_create'),
    path('maintenance/<id>/edit/', views.MaintenanceUpdateView.as_view(),name='maintenance_update'),
    path('maintenance/<id>/delete/', views.MaintenanceDeleteView.as_view(),name='maintenance_delete'),
    
    # path('ajax/enquiry/save/', views.EnquirySaveView.as_view(),name='mck_ajax_enquiry_save'),

]