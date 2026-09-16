# from django.db import models

# class tbl_Milestone(models.Model):
#     week = models.PositiveIntegerField(unique=True)
#     title = models.CharField(max_length=150)
#     description = models.TextField()
#     tips = models.TextField(blank=True)

#     class Meta:
#         db_table = 'tbl_Milestone'
#         ordering = ['week']

#     def __str__(self):
#         return self.title

# class tbl_Nutrition(models.Model):
#     name = models.CharField(max_length=150)
#     category = models.CharField(max_length=100, blank=True)
#     calories = models.FloatField(default=0)
#     protein = models.FloatField(default=0)
#     iron = models.FloatField(default=0)
#     calcium = models.FloatField(default=0)
#     fiber = models.FloatField(default=0)
#     recommendation = models.TextField(blank=True)

#     class Meta:
#         db_table = 'tbl_Nutrition'
#         ordering = ['name']

#     def __str__(self):
#         return self.name


# class tbl_Medicine(models.Model):
#     name = models.CharField(max_length=150)
#     dosage = models.CharField(max_length=100, blank=True)
#     purpose = models.TextField(blank=True)
#     warning = models.TextField(blank=True)

#     class Meta:
#         db_table = 'tbl_Medicine'

#     def __str__(self):
#         return self.name


# class tbl_Dataset(models.Model):
#     name = models.CharField(max_length=200)
#     file = models.FileField(upload_to='datasets/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     rows = models.PositiveIntegerField(default=0)
#     class Meta:
#         db_table = 'tbl_Dataset'
#         ordering = ['-uploaded_at']
#     def __str__(self):
#         return self.name

# class tbl_registration(models.Model):
#     ROLE_CHOICES = (
#         ('USER', 'User'),
#         ('DOCTOR', 'Doctor'),
#         ('ADMIN', 'Admin'),
#     )
#     user_name = models.CharField(max_length=100)
#     user_email = models.EmailField(unique=True)
#     user_contact = models.CharField(max_length=15)
#     user_address = models.TextField(blank=True, null=True)
#     user_password = models.CharField(max_length=255)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     created_at = models.DateTimeField(null=True, blank=True)
#     def __str__(self):
#         return self.user_name


# class tbl_Doctor(models.Model):
#     user = models.OneToOneField(
#         tbl_registration,
#         on_delete=models.CASCADE
#     )
#     name = models.CharField(max_length=100)
#     specialization = models.CharField(max_length=100)
#     qualification = models.CharField(max_length=100)
#     license_no = models.CharField(max_length=100)
#     experience = models.IntegerField(default=0)
#     hospital = models.CharField(max_length=200)
#     contact = models.CharField(max_length=15)

#     def __str__(self):
#         return self.name

from django.db import models


class tbl_Milestone(models.Model):
    week = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    tips = models.TextField(blank=True)

    class Meta:
        db_table = 'tbl_Milestone'
        ordering = ['week']

    def __str__(self):
        return self.title


class tbl_Nutrition(models.Model):
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=100, blank=True)
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    iron = models.FloatField(default=0)
    calcium = models.FloatField(default=0)
    fiber = models.FloatField(default=0)
    recommendation = models.TextField(blank=True)

    class Meta:
        db_table = 'tbl_Nutrition'
        ordering = ['name']

    def __str__(self):
        return self.name


class tbl_Medicine(models.Model):
    name = models.CharField(max_length=150)
    dosage = models.CharField(max_length=100, blank=True)
    purpose = models.TextField(blank=True)
    warning = models.TextField(blank=True)

    class Meta:
        db_table = 'tbl_Medicine'

    def __str__(self):
        return self.name


class tbl_Dataset(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    rows = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'tbl_Dataset'
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.name
