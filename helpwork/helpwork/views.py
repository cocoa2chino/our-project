from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from .form import User1, Task1
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
import random
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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


@csrf_exempt # 用户登录
def login(request):
    if request.method == 'GET':
        data = {
            'title': '登录',
        }
        return render(request, 'login.html', context=data)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.filter(Q(username=username) | Q(email=username))
        if users.exists():
            users = users.filter(password=password)
            if users.exists():
                user1 = users.first()
                user1.is_active = True

                user1.save()  # 登录状态修改
                request.session['username'] = user1.username
                request.session['user_id'] = user1.id
                # 第二轮之后实现，显示登录成功后几秒自动跳转到任务广场，现在先:直接到任务广场APP的视图
                return HttpResponseRedirect(reverse('task_square'))
                #return HttpResponse('发布成功')
            else:
                print('密码错误')
                return HttpResponse('密码错误')
        print('用户名不存在')
        return HttpResponse('用户名不存在')

# 注册
def index(request):
    if request.method == 'GET':
        user1 = User1()
        return render(request, 'data_form.html', locals())
    else:
        user1 = User1(request.POST, request.FILES)
        if user1.is_valid():

            user1.save()
            return render(request, 'logon_successfully.html')

        else:
            return render(request, 'data_form.html', locals())

def edit0(request):

    alphabet = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()'
    character = random.sample(alphabet, 5)
    characters=character[0]+character[1]+character[2]+character[3]+character[4]

    try:
        user_id = request.session.get('user_id')



        user = User.objects.get(id=user_id)
        user_name=user.username
        email0 =user.email
        if request.method == "POST":
        # 注意：这里由于用户名邮箱设置不能重名,所以这里的方法是调用修改后先把他改成一个其他的东西，
        # 这样子如果不修改用户名邮箱，之前的用户名邮箱就会替代这个乱码，这样可能会导致一些问题但目前还没遇到，，
            user.username = characters
            user.email = characters+'1shshhs@sjtu.edu.cn'
            user_form = User1(request.POST, request.FILES)
            user.save()
            Photo=user.icon
            context = {
            'imgs': Photo
        }
            if user_form.is_valid():
                user_cd = user_form.cleaned_data
                user.email = user_cd['email']
                user.tel = user_cd['tel']
                user.username = user_cd['username']
                user.qq = user_cd['qq']
                user.password=user_cd['password']
                user.repassword = user_cd['password']
                user.wechat = user_cd['wechat']
                user.other = user_cd['other']
                user.icon = user_cd['icon']
                user.save()
                return render(request, 'edit.html', {"user_form": user_form,"user":user})

            else:
                user.username=user_name
                user.email=email0
                user.save()
                ErrorDict = user_form.errors
                return render(request, 'edit.html', {"user_form": user_form,"user":user})
        else:

            user_form = User1(instance=user)

            return render(request, 'edit.html', {"user_form": user_form,"user":user})
    except:
        return render(request, 'no login.html')



def task_square(request):
    user_id = request.session.get('user_id')
    task_types = TaskType.objects.all()

    request.session['mclass'] = 0
    if user_id:
        username = request.session.get('username')
        tasks_list1 = Task.objects.filter(is_pickedup=False, is_overtime=False).exclude(publisher_id=user_id)
        for task in tasks_list1:
            task.soft_delete()
        tasks_list = Task.objects.filter(is_pickedup=False, is_overtime=False).exclude(publisher_id=user_id)
        paginator = Paginator(tasks_list, 9)  # Show 9 contacts per page
        page = request.GET.get('page')
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            tasks = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            tasks = paginator.page(paginator.num_pages)
        data = {
            'tasks_list': tasks_list,
            'task_types': task_types,
            'type_id': 0,
            'username': username,
            'tasks': tasks,
        }
        return render(request, 'task_square.html', context=data)
    #  新增 用户未登录时也可看广场
    else:
        tasks_list1 = Task.objects.filter(is_pickedup=False, is_overtime=False)
        for task in tasks_list1:
            task.soft_delete()
        tasks_list = Task.objects.filter(is_pickedup=False, is_overtime=False)
        paginator = Paginator(tasks_list, 9)  # Show 5 contacts per page
        page = request.GET.get('page')
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            tasks = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            tasks = paginator.page(paginator.num_pages)
        data = {
            'tasks_list': tasks_list,
            'task_types': task_types,
            'type_id': 0,
            'username': None,
            'tasks': tasks,
        }
        return render(request, 'task_square.html', context=data)


def task_square_sort(request, type_id, order):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    task_types = TaskType.objects.all()

    if order == 'task_reward':
        ordername = '按酬劳升序'
    elif order == '-task_reward':
        ordername = '按酬劳降序'
    elif order == 'ddltime':
        ordername = '按截止时间升序'
    elif order == '-ddltime':
        ordername = '按截止时间降序'
    else:
        ordername = '默认排序'

    if type_id != 0:
        sort = TaskType.objects.get(pk=type_id).typename
        if user_id:
            tasks_list1 = Task.objects.filter(is_pickedup=False, task_type=type_id, is_overtime=False).order_by(
                order).exclude(publisher_id=user_id)
            for task in tasks_list1:
                task.soft_delete()
            tasks_list = tasks_list1.filter(is_overtime=False)
        else:
            tasks_list1 = Task.objects.filter(is_pickedup=False, task_type=type_id, is_overtime=False).order_by(order)
            for task in tasks_list1:
                task.soft_delete()
            tasks_list = tasks_list1.filter(is_overtime=False)
    else:
        sort = '全部求助'
        if user_id:
            tasks_list1 = Task.objects.filter(is_pickedup=False, is_overtime=False).order_by(order).exclude(
                publisher_id=user_id)
            for task in tasks_list1:
                task.soft_delete()
            tasks_list = tasks_list1.filter(is_overtime=False)
        else:
            tasks_list1 = Task.objects.filter(is_pickedup=False, is_overtime=False).order_by(order)
            for task in tasks_list1:
                task.soft_delete()
            tasks_list = tasks_list1.filter(is_overtime=False)

    paginator = Paginator(tasks_list, 9)  # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tasks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tasks = paginator.page(paginator.num_pages)

    data = {
        'tasks': tasks,
        'username': username,
        'task_types': task_types,
        'type_id': type_id,
        'sort': sort,
        'ordername': ordername,
    }
    return render(request, 'task_square.html', context=data)

@csrf_exempt #客户端提交的post如果不加这段，tests里会出现403error
def findtasks(request):
    keywords = request.POST.get('keywords')
    user_id = request.session.get('user_id')
    task_types = TaskType.objects.all()
    if user_id:
        user = User.objects.get(pk=user_id)
        tasks = Task.objects.all().exclude(publisher_id=user_id)
        finded = []
        for task in tasks:
            if keywords in task.task_name:
                finded.append(task)
            else:
                if task.task_sketch:
                    if keywords in task.task_sketch:
                        finded.append(task)
        data = {
            'tasks': finded,
            'task_types': task_types,
            'type_id': 0,
            'username': user.username,
        }
        return render(request, 'task_square.html', context=data)
    else:
        tasks = Task.objects.all()
        finded = []
        for task in tasks:
            if keywords in task.task_name:
                finded.append(task)
            else:
                if task.task_sketch:
                    if keywords in task.task_sketch:
                        finded.append(task)
        data = {
            'tasks': finded,
            'task_types': task_types,
            'type_id': 0,
            'username': None,
        }
        return render(request, 'task_square.html', context=data)

def all_task_received(request):
    user_id = request.session.get('user_id')
    task_types = TaskType.objects.all()
    if user_id:
        task_received_list = Task.objects.filter(hunter_id=user_id)
        paginator = Paginator(task_received_list, 5)  # Show 5 contacts per page
        page = request.GET.get('page')
        try:
            task_received_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            task_received_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            task_received_list = paginator.page(paginator.num_pages)
        context = {
            'task_types': task_types,
            'task_received_list': task_received_list,
            'user_id': user_id,
        }
        return render(request, 'all_task_received.html', context)
    else:
        context = {
            'task_types': task_types,
            'task_received_list': None,
            'user_id': None,
        }
        return render(request, 'all_task_received.html', context)

def logout(request):
    request.session['username'] = None
    request.session['user_id'] = None
    return HttpResponseRedirect(reverse('task_square'))