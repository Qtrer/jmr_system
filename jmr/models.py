from django.db import models

# Create your models here.
class Enterprise(models.Model):
    enterprise_name = models.CharField(max_length=40)
    enterprise_account = models.CharField(max_length=40)
    enterprise_password = models.CharField(max_length=40)
    enterprise_address = models.CharField(max_length=80)
    enterprise_tel = models.IntegerField()
    enterprise_mail = models.EmailField()
    enterprise_info = models.CharField(max_length=200)

    def __str__(self):
        return self.enterprise_name

class Emplyee(models.Model):
    employee_name = models.CharField(max_length=40)
    employee_account = models.CharField(max_length=40)
    employee_password = models.CharField(max_length=40)
    employee_info = models.CharField(max_length=200)

    def __str__(self):
        return self.employee_name

class Job(models.Model):
    job_name = models.CharField(max_length=40)
    job_school = models.CharField(max_length=40)
    job_degree = models.CharField(max_length=40)
    job_major = models.CharField(max_length=40)
    job_salary = models.IntegerField()
    job_count = models.IntegerField()
    job_info = models.CharField(max_length=200)
    job_enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_name

class Resume(models.Model):
    resume_school = models.CharField(max_length=40)
    resume_degree = models.CharField(max_length=40)
    resume_major = models.CharField(max_length=40)
    resume_call = models.CharField(max_length=40)
    resume_employee = models.OneToOneField(Emplyee, on_delete=models.CASCADE)
    resume_job = models.ManyToManyField(Job)

    def __str__(self):
        return self.resume_employee.employee_name