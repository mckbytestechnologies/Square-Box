"""
SEO - mck P112 App
"""
from django.conf import settings


def get_page_tags(func, dynamic_seo_kwargs=None):
    """
    Build Page SEO
    """
    global_title="Total Inspection Services"
    global_description = "Total Inspection Services"
    global_keywords = """Total Inspection Services"""

    page_kwargs = {}
    if dynamic_seo_kwargs:
        title=dynamic_seo_kwargs.get('title','')
        keywords =dynamic_seo_kwargs.get('keywords','')
        description=dynamic_seo_kwargs.get('description','')

    elif func=="error_404":
        title="Page Not Found Error"
        keywords = "Page Not Found Error"
        description= "Page Not Found Error"

    elif func=="error_500":
        title="Internal Server Error"
        keywords = "Internal Server Error"
        description= "Internal Server Error"

    elif func=="downtime":
        title="Downtime"
        keywords = "Downtime"
        description= "Downtime"

    elif func=="privacy":
        title="Privacy Policy"
        keywords = "Privacy Policy,"
        description= "Privacy Policy of sk.com company website"
    
    elif func=="termsofuse":
        title="Terms of Use"
        keywords = "Terms of Use"
        description= "Terms of Use"
    
    elif func=="home_page":
        title="Building Inspection Services in Wisconsin | mck"
        description = "Get reliable building inspection services and zoning services in South Central Wisconsin with Total Inspection Services. Connect with our building inspectors!"
        keywords= "building inspection services"
        
    elif func=="company_page":
        title="Building Inspection & Zoning in Wisconsin | About TIS"
        description = "Total Inspection Services offers expert building inspection & zoning services in South Central Wisconsin. Book a building inspection now!"
        keywords= "building inspection and zoning services"
        
    elif func=="service_page":
        title="Building Permit & Inspection Services in Wisconsin | TIS"
        description = "Need permit & inspection services in South Central Wisconsin? Total Inspection Services ensures smooth approvals and compliance. Explore our services!"
        keywords= "permit and inspection services"
        
    elif func=="resources_page":
        title="Building Inspection | Resources | TIS"
        description = "Explore building inspection resources from Total Inspection Services, serving South Central Wisconsin. Stay informed with expert insights! "
        keywords= "building inspection"
        
    elif func=="faq_page":
        title="Building & Municipal Inspection | Wisconsin | TIS "
        description = "Total Inspection Services ensures safe and compliant municipal & building inspections in South Central Wisconsin.Reach out to us!"
        keywords= "building and municipal inspection"
    
    elif func=="contact_us_page":
        title="Building Inspection Services In Wisconsin | Contact TIS"
        description = "Get in touch with Total Inspection Services for expert building inspection services in South Central Wisconsin. Contact us today to schedule an inspection! "
        keywords= "building Inspection services "
        
    elif func=="request_an_inspection_page":
        title="Building Inspection Services In Wisconsin I TIS "
        description = "Schedule a professional building inspection services with Total Inspection Services in South Central Wisconsin.Get expert evaluations and detailed reports."
        keywords= "building inspection services"
        
    elif func=="apply_for_permit_page":
        title="Building Permit Services in Wisconsin I TIS "
        description = "Apply for building permits hassle-free with Total Inspection Services in South Central Wisconsin. Get your permits approved smoothly! "
        keywords= "building permit services"
        
    else:
        title=global_title
        keywords = global_keywords
        description= global_description

    page_kwargs["title"] = title
    page_kwargs["keywords"] = keywords
    page_kwargs["description"] = description
    page_kwargs["media_url"]= settings.MEDIA_STATIC_URL
    page_kwargs["uploaded_url"]= settings.MEDIA_URL
    page_kwargs["function"] = func

    return page_kwargs
