from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from config import app_gv as gv


class FAQCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)
    
    class Meta:
        db_table = 'faqcategory'

    def __str__(self):
        return self.name


class FAQ(models.Model):
    faqcategory = models.ForeignKey(FAQCategory, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = models.TextField()
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)
    
    class Meta:
        db_table = 'faq'

    def __str__(self):
        return self.question


class County(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)
    
    class Meta:
        db_table = 'county'

    def __str__(self):
        return self.name


class Area(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE,)
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField()
    tag = MultiSelectField(choices=gv.TAG_CHOICES, blank=True)
    link = models.URLField(blank=True, null=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    class Meta:
        db_table = 'area'

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True , help_text="Upload image with 1:1 aspect ratio(100px x 100px) ")
    tags = models.CharField(max_length=255, blank=True, null=True)
    star = models.IntegerField(default=5)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    class Meta:
        db_table = 'testimonial'

    def __str__(self):
        return f"{self.name} - {self.area.name}"
