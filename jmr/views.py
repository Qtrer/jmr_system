from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from jmr.models import *
from jmr.forms import *

# Create your views here.

def login(request):
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('user_name')
            password = login_form.cleaned_data.get('user_password')

            try:
                user = models.JobHunter.objects.get(userName=username)
            except:
                message = '用户不存在！'
                return render(request, 'login.html', locals())

            if user.password == password:
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())

    login_form = UserForm()
    return render(request, 'login.html', locals())

def employeeIndex(request, id):
    employee = Employee.objects.get(id=id)
    resume = Resume.objects.get(resume_employee_id=id)
    jobs = Job.objects.all()
    recommendedJobs = Job.objects.filter(job_major=resume.resume_major).filter(job_degree__lte=resume.resume_degree)
    context = { 'employee': employee, 'resume': resume, 'jobs': jobs, 'recommendedJobs': recommendedJobs }
    return render(request, 'employee/index-emlpoyee.html', context)

def employeeUpdate(request, id):
    employee = Employee.objects.get(id=id)
    context = {'employee': employee}
    employee_form = EmployeeForm()
    employee_form.fields['employee_name'].initial = employee.employee_name
    employee_form.fields['employee_account'].initial = employee.employee_account
    employee_form.fields['employee_password'].initial = employee.employee_password
    return render(request, 'employee/edit/employee_update.html', locals())

def employeeUpdateHandler(request, id):
    employee_name = request.POST.get('employee_name')
    employee_account = request.POST.get('employee_account')
    employee_password = request.POST.get('employee_password')
    employee = Enterprise.objects.get(id=id)
    employee.employee_name = employee_name
    employee.employee_account = employee_account
    employee.employee_password = employee_password
    return redirect(reverse('employeeIndex', args=(id,)))

def resumeUpdate(request, id):
    resume = Resume.objects.get(resume_employee_id=id)
    context = {'resume': resume}
    resume_form = ResumeForm()
    resume_form.fields['resume_birthday'].initial = resume.resume_birthday
    resume_form.fields['resume_race'].initial = resume.resume_race
    resume_form.fields['resume_school'].initial = resume.resume_school
    resume_form.fields['resume_major'].initial = resume.resume_major
    resume_form.fields['resume_degree'].initial = resume.resume_degree
    resume_form.fields['resume_address'].initial = resume.resume_address
    resume_form.fields['resume_tel'].initial = resume.resume_tel
    resume_form.fields['resume_mail'].initial = resume.resume_mail
    resume_form.fields['resume_info'].initial = resume.resume_info
    return render(request, 'employee/edit/resume_update.html', locals())

def resumeUpdateHandler(request, id):
    resume_name = request.POST.get('resume_name')
    resume_race = request.POST.get('resume_race')
    resume_school = request.POST.get('resume_school')
    resume_major = request.POST.get('resume_major')
    resume_degree = request.POST.get('resume_degree')
    resume_address = request.POST.get('resume_address')
    resume_tel = request.POST.get('resume_tel')
    resume_mail = request.POST.get('resume_mail')
    resume_info = request.POST.get('resume_info')
    resume = Resume.objects.get(resume_employee_id=id)
    resume.resume_name = resume_name
    resume.resume_race = resume_race
    resume.resume_school = resume_school
    resume.resume_major = resume_major
    resume.resume_degree = resume_degree
    resume.resume_address = resume_address
    resume.resume_tel = resume_tel
    resume.resume_mail = resume_mail
    resume.resume_info = resume_info
    resume.save()
    return redirect(reverse('employeeIndex', args=(id,)))

def enterpriseList(request):
    enterprises = Enterprise.objects.all()
    context = {'enterprises': enterprises}
    return render(request, 'enterprise/list.html',context)

def enterpriseDetail(request, id):
    enterprise = Enterprise.objects.get(id = id)
    jobs = Job.objects.filter(job_enterprise_id = id)
    context = { 'enterprise': enterprise, 'jobs': jobs }
    return render(request, 'enterprise/detail.html',context)

def enterpriseIndex(request, id):
    enterprise = Enterprise.objects.get(id = id)
    jobs = Job.objects.filter(job_enterprise_id = id)
    resumes = Resume.objects.all()
    for job in jobs:
        recommendedResumes = Resume.objects.filter(resume_major=job.job_major).filter(resume_degree__gte=job.job_degree)
    context = { 'enterprise': enterprise, 'jobs': jobs, 'resumes': resumes, 'recommendedResumes': recommendedResumes }
    return render(request, 'enterprise/index-enterprise.html',context)

def enterpriseJobs(request, id):
    enterprise = Enterprise.objects.get(id = id)
    jobs = Job.objects.filter(job_enterprise_id = id)
    context = { 'enterprise': enterprise, 'jobs': jobs }
    return render(request, 'enterprise/enterprise_job.html',context)

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
    enterprise.enterprise_name = enterprise_name
    enterprise.enterprise_account = enterprise_account
    enterprise.enterprise_password = enterprise_password
    enterprise.enterprise_address = enterprise_address
    enterprise.enterprise_tel = enterprise_tel
    enterprise.enterprise_mail = enterprise_mail
    enterprise.enterprise_info = enterprise_info
    enterprise.save()
    return redirect(reverse('enterpriseDetail', args=(id,)))

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
    return redirect(reverse('enterpriseJobs', args=(id,)))

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
    return redirect(reverse('enterpriseJobs', args=(id,)))

def enterpriseDeleteJob(request, id, jid):
    job = Job.objects.get(id=jid)
    job.delete()
    return redirect(reverse('enterpriseJobs', args=(id,)))

def jobList(request):
    jobs = Job.objects.all()
    context = {'jobs': jobs}
    return render(request, 'job/list.html',context)

def jobDetail(request, id):
    job = Job.objects.get(id = id)
    context = { 'job': job }
    return render(request, 'job/detail.html',context)

def resumeDetail(request, id):
    resume = Resume.objects.get(resume_employee_id = id)
    context = { 'resume': resume }
    return render(request, 'resume/detail.html',context)

def resumeSend(request, id, jid):
    resume = Resume.objects.get(resume_employee_id=id)
    job = Job.objects.get(id=jid)
    job.job_resume.add(resume)
    return redirect(reverse('resumeSended', args=(id,)))

def resumeSended(request, id):
    resume = Resume.objects.get(resume_employee_id=id)
    jobs = resume.job_set.all()
    jobs_resumes = Jobs_Resumes.objects.filter(resume=resume, isEmploy=True)
    return render(request, 'employee/resume_send.html', locals())

def resumeReceive(request, id, jid, rid):
    enterprise = Enterprise.objects.get(id=id)
    job = Job.objects.get(id=jid)
    resumes = job.job_resume.all()
    jobs_resumes = Jobs_Resumes.objects.get(job_id=jid, resume_id=rid)
    jobs_resumes.isEmploy = True
    jobs_resumes.save()
    return redirect(reverse('resumeReceived', args=(id,)))

def resumeRefuse(request, id, jid, rid):
    enterprise = Enterprise.objects.get(id=id)
    job = Job.objects.get(id=jid)
    resumes = job.job_resume.all()
    jobs_resumes = Jobs_Resumes.objects.get(job_id=jid, resume_id=rid)
    jobs_resumes.delete()
    return redirect(reverse('resumeReceived', args=(id,)))

def resumeReceived(request, id):
    enterprise = Enterprise.objects.get(id=id)
    jobs = Job.objects.filter(job_enterprise_id=id)
    lists = []
    for job in jobs:
        resumes = job.job_resume.all()
        for resume in resumes:
            jobs_resumes = Jobs_Resumes.objects.get(job=job, resume=resume)
            lists.append(jobs_resumes)
    jobs_resumes_employed = Jobs_Resumes.objects.filter(job__in=jobs, isEmploy=True)
    return render(request, 'enterprise/resume_receive.html', locals())

