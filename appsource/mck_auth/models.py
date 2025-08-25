import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from config import app_gv as gv
from mck_master.models import MasterPermission


class User(AbstractUser):
    mobile_number = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        if self.username:
            return self.username
        elif self.first_name:
            return self.first_name+" "+self.last_name
        elif self.email:
            return self.email
        elif self.mobile_number:
            return self.mobile_number.as_international
        else:
            return "User-"+str(self.id)


class AccountType(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=6, unique=True, db_index=True)
    is_default = models.BooleanField(default=False)
    is_registration_allowed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'account_type'


class AccountTypeRole(models.Model):
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,related_name = "%(class)s_createdby", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User,related_name = "%(class)s_updatedby", on_delete=models.CASCADE)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        db_table = 'account_type_role'


class AccountTypeRolePermission(models.Model):
    account_type_role = models.ForeignKey(AccountTypeRole, on_delete=models.CASCADE)
    master_permission = models.ForeignKey(MasterPermission, on_delete=models.CASCADE)
    has_permission = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,related_name = "%(class)s_createdby", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User,related_name = "%(class)s_updatedby", on_delete=models.CASCADE)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return f"{self.account_type_role.name} - {self.master_permission.class_name} - {self.has_permission}"

    class Meta:
        db_table = 'account_type_role_permission'


class Account(models.Model):
    uid = models.CharField(max_length=20, unique=True, editable=False, db_index=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, db_index=True)
    created_by = models.ForeignKey(User, related_name="%(class)s_createdby", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}({1})".format(self.name, self.uid)

    def save(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)
        if not self.uid:
            self.uid  = "mck-A%04d" % (int(self.id))
            super(Account, self).save()

    class Meta:
        db_table = 'account'


class AccountUser(models.Model):
    uid = models.CharField(max_length=20, unique=True, editable=False, db_index=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(AccountTypeRole, on_delete=models.CASCADE)
    is_default_account = models.BooleanField(default=True)
    is_current_account = models.BooleanField(default=True)
    last_active_on = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='%(class)s_created_by', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}({1})".format(self.user.first_name, self.uid)

    def save(self):
        super(AccountUser, self).save()
        if not self.uid:
            self.uid  = "mck-AU%04d" % (int(self.id))
            super(AccountUser, self).save()

    class Meta:
        db_table = 'account_user'
