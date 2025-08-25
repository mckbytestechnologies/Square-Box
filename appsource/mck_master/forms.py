from django import forms
from crispy_forms.helper import FormHelper
from django.shortcuts import redirect
from crispy_forms.layout import Layout, Fieldset, ButtonHolder
from crispy_forms.helper import *
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from mck_master import models


class SupportPageContentCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super(SupportPageContentCreateUpdateForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = "form-control form-control-solid"
        
        if mode == "edit":
            instance = kwargs.get('instance', None)
        save_button_name = "SAVE"

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                
                Row(Column(Field('support_key')), css_class='col-12'),
                Row(Column(Field('support_value')), css_class='col-12'),
                Row(Column(Field('support_description')), css_class='col-12'),
                Row(Column(Field('content_type')), css_class='col-12'),
            ),
            ButtonHolder(
                Div(HTML('<a class="btn btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),Submit('create_button', save_button_name, css_class='btn btn-lg btn-primary'),
                            css_class="d-flex text-right justify-content-end pt-10 col-12"), css_class="row col-12 pe-5",
            )
        )
    class Meta:
        model = models.SupportPageContent
        exclude = ['image', 'created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


class CategoryCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super(CategoryCreateUpdateForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = "form-control form-control-solid"
        
        if mode == "edit":
            instance = kwargs.get('instance', None)
        save_button_name = "SAVE"

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Row(Column(Field('name')), Column(Field('image')), css_class='col-12'),
            ),
            ButtonHolder(
                Div(HTML('<a class="btn btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),Submit('create_button', save_button_name, css_class='btn btn-lg btn-primary'),
                            css_class="d-flex text-right justify-content-end pt-10 col-12"), css_class="row col-12 pe-5",
            )
        )
    class Meta:
        model = models.Category
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


class SubCategoryCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super(SubCategoryCreateUpdateForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = "form-control form-control-solid"
        
        if mode == "edit":
            instance = kwargs.get('instance', None)
        save_button_name = "SAVE"

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Row(Column(Field('category', css_class="form-select form-select-lg form-select-solid", data_control='select2',)), Column(Field('name')), Column(Field('image')), css_class='col-12'),
            ),
            ButtonHolder(
                Div(HTML('<a class="btn btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),Submit('create_button', save_button_name, css_class='btn btn-lg btn-primary'),
                            css_class="d-flex text-right justify-content-end pt-10 col-12"), css_class="row col-12 pe-5",
            )
        )
    class Meta:
        model = models.SubCategory
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


class BannerCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super(BannerCreateUpdateForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = "form-control form-control-solid"
        
        if mode == "edit":
            instance = kwargs.get('instance', None)
        save_button_name = "SAVE"

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Row(Column(Field('name')), Column(Field('image')), css_class='col-12'),
            ),
            ButtonHolder(
                Div(HTML('<a class="btn btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),Submit('create_button', save_button_name, css_class='btn btn-lg btn-primary'),
                            css_class="d-flex text-right justify-content-end pt-10 col-12"), css_class="row col-12 pe-5",
            )
        )
    class Meta:
        model = models.Banner
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


class GalleryCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super(GalleryCreateUpdateForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = "form-control form-control-solid"
        
        if mode == "edit":
            instance = kwargs.get('instance', None)
        save_button_name = "SAVE"

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Row(Column(Field('name')), Column(Field('image')), css_class='col-12'),
            ),
            ButtonHolder(
                Div(HTML('<a class="btn btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),Submit('create_button', save_button_name, css_class='btn btn-lg btn-primary'),
                            css_class="d-flex text-right justify-content-end pt-10 col-12"), css_class="row col-12 pe-5",
            )
        )
    class Meta:
        model = models.Gallery
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


# State
class StateCreateUpdateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super(StateCreateUpdateForm, self).__init__(*args, **kwargs)
        self.fields['country'].empty_label = "Please select"

        # Apply Bootstrap styles to all fields
        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = "form-control form-control-solid"
        
        # If edit mode, handle instance
        if mode == "edit":
            instance = kwargs.get('instance', None)

        save_button_name = "SAVE"

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Row(Column(Field('name')), Column(Field('code')), css_class='col-12'),
                Row(Column(Field('country')), css_class='col-12'),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', save_button_name, css_class='btn btn-lg btn-primary'),
                    css_class="d-flex text-right justify-content-end pt-10 col-12"
                ),
                css_class="row col-12 pe-5 mt-3",
            )
        )

    class Meta:
        model = models.State
        exclude = ['created_on', 'updated_on', 'datamode']


# City
class CityCreateUpdateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super(CityCreateUpdateForm, self).__init__(*args, **kwargs)
        self.fields['state'].empty_label = "Please select"
        
        # Apply Bootstrap styles to all fields
        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = "form-control form-control-solid"
        
        # If edit mode, handle instance
        if mode == "edit":
            instance = kwargs.get('instance', None)
        save_button_name = "SAVE"

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Row(Column(Field('name')), Column(Field('code')), css_class='col-12'),
                Row(Column(Field('state')), css_class='col-12'),
            ),
            ButtonHolder(
                Div(HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', save_button_name, css_class='btn btn-lg btn-primary'),
                    css_class="d-flex text-right justify-content-end pt-10 col-12"),
                css_class="row col-12 pe-5 mt-3",
            )
        )

    class Meta:
        model = models.City
        exclude = ['created_on', 'updated_on', 'datamode']


class OfferCreateUpdateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super(OfferCreateUpdateForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = "form-control form-control-solid"
        
        if mode == "edit":
            instance = kwargs.get('instance', None)
        save_button_name = "SAVE"

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Row(
                    Column(Field('name')),  
                    Column(Field('image')),  
                    css_class='col-12'
                ),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', save_button_name, css_class='btn btn-lg btn-primary'),
                    css_class="d-flex text-right justify-content-end pt-10 col-12"
                ), 
                css_class="row col-12 pe-5",
            )
        )

    class Meta:
        model = models.Offers
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']
        

class ClientFeedbackCreateUpdateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super(ClientFeedbackCreateUpdateForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = "form-control form-control-solid"
        
        if mode == "edit":
            instance = kwargs.get('instance', None)
        save_button_name = "SAVE"

        # Form layout using crispy-forms
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Row(
                    Column(Field('name')),  
                    Column(Field('feedback')),
                    css_class='col-12'
                ),
                Row(
                    Column(Field('image')),  
                    Column(Field('place')),
                    css_class='col-12'
                ),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', save_button_name, css_class='btn btn-lg btn-primary'),
                    css_class="d-flex text-right justify-content-end pt-10 col-12"
                ),
                css_class="row col-12 pe-5 mt-3",
            )
        )

    class Meta:
        model = models.ClientFeedback
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']
