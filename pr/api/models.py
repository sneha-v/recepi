from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

USER_TYPE = ((1,"RECRUITER"),(2,"STUDENT"))

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    user_type = models.IntegerField(choices=USER_TYPE, default=1)

class Organisation(models.Model):
    admin_name = models.ForeignKey(User,on_delete=models.CASCADE)
    organ_name = models.CharField(max_length = 100)
    about_company = models.TextField()

    def __str__(self):
        return self.organ_name

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stu_name = models.CharField(max_length = 100)
    age = models.IntegerField(default = 20)
    sslc_percent = models.IntegerField(default = 50)
    pu_percent = models.IntegerField(default = 50)
    degree = models.CharField(max_length = 100)
    course_name = models.CharField(max_length = 100)
    aggregate = models.FloatField(default = 5.5)
    about_me = models.TextField()
    skills = ArrayField(models.CharField(max_length = 100))
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return self.stu_name

class JobPosting(models.Model):
    company =models.ForeignKey(Organisation, on_delete=models.CASCADE)
    role_name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100)
    who_can_apply = models.TextField()
    salary = models.IntegerField(default=1000)
    skills_req = ArrayField(models.CharField(max_length = 100))
    apply_by = models.DateField(auto_now = True)
    vacancy = models.IntegerField(default = 1)

    def __str__(self):
        return self.role_name

class ApplicationStatus(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete = models.CASCADE, default=0)
    job_posting = models.ForeignKey(JobPosting,on_delete = models.CASCADE)
    status = models.CharField(max_length = 1)
