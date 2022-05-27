from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from .form import User1, Task1
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
import random
from .models import *


def task_up(request):
    if request.method == 'GET':
        task1 = Task1()
        return render(request, 'task_form.html', locals())
    else:
        task1 = Task1(request.POST, request.FILES)
        if task1.is_valid():
            try:
                user_id = request.session.get('user_id')
                user = User.objects.get(pk=user_id)
                contactid = request.POST.get('contact_type_publisher')
                contactname = Contact.objects.get(pk=contactid).typename

                task1.cleaned_data['publisher_id'] = user_id
                if getattr(user, contactname) == None:
                #return render(request, 'hunt/task_form.html', locals())
                    return render(request, 'task_nocontact.html', context={'task': task1,
                                                                      'contactname': contactname, })
            except:
                return render(request, 'no login.html')

            else:
                Task.objects.create(**task1.cleaned_data)
                return render(request, 'task_up_successfully.html', locals())
        else:
            return render(request, 'task_form.html', locals())