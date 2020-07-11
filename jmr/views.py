from django.shortcuts import render, redirect
from django.urls import reverse
from jmr.models import *
from jmr.forms import *

# Create your views here.

def login(request):
    return render(request, 'login.html')

def enterpriseList(request):
    enterprises = Enterprise.objects.all()
    context = {'enterprises': enterprises}
    return render(request, 'enterprise/list.html',context)

def enterpriseDetail(request, id):
    enterprise = Enterprise.objects.get(id = id)
    jobs = Job.objects.filter(job_enterprise_id = id)
    context = { 'enterprise': enterprise, 'jobs': jobs }
    return render(request, 'enterprise/detail.html',context)

def enterpriseUpdate(request, id):
    enterprise = Enterprise.objects.get(id=id)
    context = { 'enterprise': enterprise }
    enterprise_form = EnterpriseForm()
    enterprise_form.fields['enterprise_name'].initial = enterprise.enterprise_name
    enterprise_form.fields['enterprise_account'].initial = enterprise.enterprise_account
    enterprise_form.fields['enterprise_password'].initial = enterprise.enterprise_password
    enterprise_form.fields['enterprise_address'].initial = enterprise.enterprise_address
    enterprise_form.fields['enterprise_tel'].initial = enterprise.enterprise_tel
    enterprise_form.fields['enterprise_mail'].initial = enterprise.enterprise_mail
    enterprise_form.fields['enterprise_info'].initial = enterprise.enterprise_info
    return render(request, 'enterprise/edit/enterprise_update.html',locals())

def enterpriseUpdateHandler(request, id):
    enterprise_name = request.POST.get('enterprise_name')
    enterprise_account = request.POST.get('enterprise_account')
    enterprise_password = request.POST.get('enterprise_password')
    enterprise_address = request.POST.get('enterprise_address')
    enterprise_tel = request.POST.get('enterprise_tel')
    enterprise_mail = request.POST.get('enterprise_mail')
    enterprise_info = request.POST.get('enterprise_info')
    enterprise = Enterprise.objects.get(id=id)
    enterprise.job_name = enterprise_name
    enterprise.job_school = enterprise_account
    enterprise.job_degree = enterprise_password
    enterprise.job_major = enterprise_address
    enterprise.job_salary = enterprise_tel
    enterprise.job_count = enterprise_mail
    enterprise.job_info = enterprise_info
    enterprise.save()
    return redirect(reverse('enterpriseList'))

def enterpriseAddJob(request, id):
    enterprise = Enterprise.objects.get(id=id)
    context = { 'enterprise': enterprise }
    job_form = JobForm()
    return render(request, 'enterprise/edit/job_add.html',locals())

def enterpriseAddJobHandler(request, id):
    job_name = request.POST.get('job_name')
    job_school = request.POST.get('job_school')
    job_degree = request.POST.get('job_degree')
    job_major = request.POST.get('job_major')
    job_salary = request.POST.get('job_salary')
    job_count = request.POST.get('job_count')
    job_info = request.POST.get('job_info')
    job = Job()
    job.job_name = job_name
    job.job_school = job_school
    job.job_degree = job_degree
    job.job_major = job_major
    job.job_salary = job_salary
    job.job_count = job_count
    job.job_info = job_info
    job.job_enterprise_id = id
    job.save()
    return redirect(reverse('jobList'))

def enterpriseUpdateJob(request, id, jid):
    enterprise = Enterprise.objects.get(id=id)
    job = Job.objects.get(id=jid)
    context = { 'enterprise': enterprise, 'job': job }
    job_form = JobForm()
    job_form.fields['job_name'].initial = job.job_name
    job_form.fields['job_school'].initial = job.job_school
    job_form.fields['job_degree'].initial = job.job_degree
    job_form.fields['job_major'].initial = job.job_major
    job_form.fields['job_salary'].initial = job.job_salary
    job_form.fields['job_count'].initial = job.job_count
    job_form.fields['job_info'].initial = job.job_info
    return render(request, 'enterprise/edit/job_update.html',locals())

def enterpriseUpdateJobHandler(request, id, jid):
    job_name = request.POST.get('job_name')
    job_school = request.POST.get('job_school')
    job_degree = request.POST.get('job_degree')
    job_major = request.POST.get('job_major')
    job_salary = request.POST.get('job_salary')
    job_count = request.POST.get('job_count')
    job_info = request.POST.get('job_info')
    job = Job.objects.get(id=jid)
    job.job_name = job_name
    job.job_school = job_school
    job.job_degree = job_degree
    job.job_major = job_major
    job.job_salary = job_salary
    job.job_count = job_count
    job.job_info = job_info
    job.save()
    return redirect(reverse('jobList'))

def enterpriseDeleteJob(request, id, jid):
    job = Job.objects.get(id=jid)
    job.delete()
    return redirect(reverse('jobList'))

def jobList(request):
    jobs = Job.objects.all()
    context = {'jobs': jobs}
    return render(request, 'job/list.html',context)

def jobDetail(request, id):
    job = Job.objects.get(id = id)
    context = { 'job': job }
    return render(request, 'job/detail.html',context)
