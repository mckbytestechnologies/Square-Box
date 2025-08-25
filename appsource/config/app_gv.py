

DATAMODE_CHOICES = (('A','Active'),('I','Inactivated'),('D','Deleted'))
APP_LIST = (('CUS_IOS_APP', 'IOS App'), ('CUS_ANDROID_APP', 'Android App'))
SALUTATION_TYPE = (("mr", "Mr."), ("mrs", "Mrs."),("ms", "Ms."))
GENDER = (('MALE','Male'),('FEMALE','Female'),('OTHERS','Others'))

Active = 'Active'
Replaced_new_staff = 'Replaced New Staff'
Terminated = 'terminated'

SOCIAL_ACCOUNT = (("FACEBOOK", "Facebook"),
                  ("TWITTER","Twitter"),
                  ("THREADS","Threads"),
                  ("YOUTUBE","Youtube"),
                  ("INSTAGRAM","Instagram"))

UPI_VENDOR = (("GPAY", "GPay"),
              ("PHONEPE", "PhonePe"),
              ("PAYTM", "Paytm"),
              ("CRED", "Cred"))

ENQUIRY_STATUS = (("OPEN", ""),
                  ("INPROGRESS", "InProgress"),
                  ("CLOSED", "Closed"))

IMAGE_REPO_FOLDER = 'data/ir'
FILE_REPO_FOLDER = 'data/fr'

INVOICE_STATUS = (('DUE', 'Due'), ('PAID', 'Paid'), ('PARTIALLY', 'Partially Paid'))
PAYMENT_TRANSACTION_MODE = (('CASH','Cash'), ('CARD','Card'), ('UPI','UPI'))

TAG_CHOICES = [
    ("BULDING INSPECTION AND PERMITS", "Building Inspection and Permits"),
    ("ZONING", "Zoning"),
    ("COMMERCIAL", "Commercial"),
]

TYPE_CHOICES = [
        ('DOCUMENT', 'Document'),
        ('LINK', 'Link'),
    ]

INSPECTION_TYPE = (
    ("footings", "Footings"),
    ("foundation", "Foundation"),
    ("in-floor_plumbing", "In-floor Plumbing"),
    ("vapor_barrier_basement", "Vapor Barrier Basement"),
    ("rough_construction", "Rough Construction"),
    ("rough_electrical", "Rough Electrical"),
    ("rough_plumbing", "Rough Plumbing"),
    ("rough_hvac", "Rough HVAC"),
    ("insulation", "Insulation"),
    ("electric_service", "Electric Service"),
    ("occupancy_final", "Occupancy / Final"),
    ("temp_electrical_service", "Temp Electrical Service")
)

PROPERTY_TYPE_CHOICES = (
    ("APARTMENT", "Apartment"),
    ("VILLA", "Villa"),
    ("INDEPENDENT_HOUSE", "Independent House"),
    ("PLOT", "Plot / Land"),
    ("COMMERCIAL", "Commercial Property"),
    ("STUDIO", "Studio Apartment"),
)
