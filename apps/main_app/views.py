from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

from .models import *


###---GET---------------------------INDEX ROUTE
def index(request):
    try:
        user = User.objects.get(id=request.session['user_id'])
        context = {
                "jobs": Job.objects.exclude(assigned_to=user),
                "myjobs": Job.objects.filter(assigned_to=user)
        }
        return render(request, 'main_app/index.html', context)
    except:
        return redirect('/')


###---GET---------------------------NEW ROUTE
def new(request):
    context = {
        "categories": Category.objects.all()
    }

    return render(request, 'main_app/new.html', context)


###---GET---------------------------VIEW ROUTE
def show(request,id):
    context = {
        "job": Job.objects.get(id=id),
        "categories": Job.objects.get(id=id).has_category.all()
    }


    return render(request, 'main_app/show.html', context)


###---GET---------------------------EDIT ROUTE
def edit(request,id):
    context = {
        "job": Job.objects.get(id=id),
        "categories": Job.objects.get(id=id).has_category.all()
    }


    return render(request, 'main_app/edit.html', context)



###---POST---------------------------CREATE ROUTE
def create(request):
 
    joberrors =  Job.objects.basic_validator(request.POST)   
    if len(joberrors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main/new')    
    else:
        user = User.objects.get(id=request.session['user_id'])
        new_job = Job.objects.create(
                title = request.POST['title'],
                description = request.POST['description'],
                location = request.POST['location'],
                added_by = user
        )

        this_category = request.POST['category']         
        this_job = new_job
        this_job.has_category.add(this_category)

        #if newcategory was added
        if request.POST['newcategory'] != '':
                errors = Category.objects.basic_validator(request.POST)
                if len(errors):
                        for key, value in errors.items():
                                messages.error(request, value)
                        return redirect('/main/new')

                new_category = Category.objects.create(
                        category_name = request.POST['newcategory']
                )

                this_category = new_category         
                this_job.has_category.add(this_category)


        messages.add_message(
            request, messages.SUCCESS,
            'The job has been stored.'
        )

    return redirect('/main')

###---POST------------------------------DESTROY ROUTE
def destroy(request,id):
    try:
        user = User.objects.get(id=request.session['user_id'])
        checkowner = Job.objects.get(id=id, added_by=user) 
        if checkowner:
            Job.objects.get(id=id).delete()
            print("Deleted wish_id = " + id)

            return redirect('/main')
    except:
        messages.add_message(
            request, messages.ERROR,
            "You cannot delete a job you did not create."
        )
            
        return redirect('/main')


###---POST------------------------------UPDATE ROUTE
def update(request):
    joberrors =  Job.objects.basic_validator(request.POST)   
    if len(joberrors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main/new')    

    else:        
        j = Job.objects.get(id=request.POST['job_id'])
        j.title = request.POST['title']
        j.description = request.POST['description']
        j.location = request.POST['location']
        j.save()

        return redirect('/main')


###---POST-------------------------------CLAIM A JOB
def claim(request,id):
        user = User.objects.get(id=request.session['user_id'])
        j = Job.objects.get(id=id)
        j.assigned_to = user
        j.save()

        return redirect('/main')

###---POST-------------------------------GIVE UP A JOB
def refuse(request,id):
        user = User.objects.get(id=request.session['user_id'])
        
        j = Job.objects.get(id=id)
        j.assigned_to = None
        j.save()

        return redirect('/main')


