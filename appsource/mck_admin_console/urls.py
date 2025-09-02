
from django.urls import path
from mck_admin_console import views

app_name = "mck_admin_console"

urlpatterns = [
    path('', views.LandingPage.as_view(), name='mck_landing_page'),
    path('dashboard/', views.DashboardView.as_view(), name='mck_dashboard'),
    
    path('faq_category/list/', views.FAQCategoryList.as_view(),name='mck_faq_category_list'),
    path('faq_category/create/', views.FAQCategoryCreateView.as_view(),name='mck_faq_category_create'),
    path('faq_category/<id>/edit/', views.FAQCategoryUpdateView.as_view(),name='mck_faq_category_update'),
    path('faq_category/<id>/delete/', views.FAQCategoryDeleteView.as_view(),name='mck_faq_category_delete'),
    
    path('faq/list/', views.FAQList.as_view(),name='mck_faq_list'),
    path('faq/create/', views.FAQCreateView.as_view(),name='mck_faq_create'),
    path('faq/<id>/edit/', views.FAQUpdateView.as_view(),name='mck_faq_update'),
    path('faq/<id>/delete/', views.FAQDeleteView.as_view(),name='mck_faq_delete'),
    
    path('area/list/', views.AreaListView.as_view(), name='mck_area_list'),
    path('area/create/', views.AreaCreateView.as_view(), name='mck_area_create'),
    path('area/<id>/edit/', views.AreaUpdateView.as_view(), name='mck_area_update'),
    path('area/<id>/delete/', views.AreaDeleteView.as_view(), name='mck_area_delete'),
    
    path('testimonial/list/', views.TestimonialListView.as_view(), name='mck_testimonial_list'),
    path('testimonial/create/', views.TestimonialCreateView.as_view(), name='mck_testimonial_create'),
    path('testimonial/<id>/edit/', views.TestimonialUpdateView.as_view(), name='mck_testimonial_update'),
    path('testimonial/<id>/delete/', views.TestimonialDeleteView.as_view(), name='mck_testimonial_delete'),

]