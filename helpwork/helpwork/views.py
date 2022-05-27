import os

from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from . import settings
from .form import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
import random
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def task_up(request):
    if request.method == 'GET':
        task1 = Task1()
        return render(request, 'hunt/task_form.html', locals())
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
                    return render(request, 'hunt/task_nocontact.html', context={'task': task1,
                                                                      'contactname': contactname, })
            except:
                return render(request, 'hunt/no login.html')

            else:
                Task.objects.create(**task1.cleaned_data)
                return render(request, 'hunt/task_up_successfully.html', locals())
        else:
            return render(request, 'hunt/task_form.html', locals())

def taskcopy(request):
    taskid0 = request.session.get('task_id')
    task = Task.objects.filter(task_id=taskid0)
    task.publisher_id = request.session.get('user_id')
    task.save()

@csrf_exempt # 用户登录
def login(request):
    if request.method == 'GET':
        data = {
            'title': '登录',
        }
        return render(request, 'hunt/login.html', context=data)
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
        return render(request, 'hunt/data_form.html', locals())
    else:
        user1 = User1(request.POST, request.FILES)
        if user1.is_valid():

            user1.save()
            return render(request, 'hunt/logon_successfully.html')

        else:
            return render(request, 'hunt/data_form.html', locals())

# 个人信息显示与修改
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
                return render(request, 'hunt/edit.html', {"user_form": user_form,"user":user})

            else:
                user.username=user_name
                user.email=email0
                user.save()
                ErrorDict = user_form.errors
                return render(request, 'hunt/edit.html', {"user_form": user_form,"user":user})
        else:

            user_form = User1(instance=user)

            return render(request, 'hunt/edit.html', {"user_form": user_form,"user":user})
    except:
        return render(request, 'hunt/no login.html')

# 进入“我接受的任务”按钮
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
        return render(request, 'task_received/all_task_received.html', context)
    else:
        context = {
            'task_types': task_types,
            'task_received_list': None,
            'user_id': None,
        }
        return render(request, 'task_received/all_task_received.html', context)


# ?好像没用到？不敢删
def task_revoke(request, task_id):
    username = request.session.get('username')
    user = User.objects.get(username=username)
    target_task = Task.objects.get(pk=task_id)
    target_task.is_pickedup = False
    target_task.hunter = None
    target_task.contact_type_hunter = None
    target_task.save()
    return HttpResponseRedirect(reverse('all_task_received'))


def reasons_revoke(request, task_id):
    task = Task.objects.get(pk=task_id)
    request.session['task_id'] = task_id
    return render(request, 'task_received/reasons_revoke.html', context={'task_id': task_id, 'task': task})


def revoke(request):
    reason = Revoke_reason()
    task = Task.objects.get(pk=request.session.get('task_id'))
    reason.task = task
    reason.revoke_reason = request.POST.get('reasons')
    task.is_pickedup = False
    task.hunter_id = None
    task.contact_type_hunter = None
    task.save()
    reason.save()
    return render(request, 'task_received/comment_or_revoke_successfuly.html',
                  context={'task': task, 'comment': 0, 'revoke': 1})


def task_detail(request, task_id):
    username = request.session.get('username')
    user = User.objects.get(username=username)
    task = Task.objects.get(pk=task_id)
    contact = task.contact_type_publisher.typename
    contact = getattr(user, contact)
    return render(request, 'task_received/task_detail.html', context={'task': task,
                                                                      'contact': contact})



def task_finished(request, task_id):
    task = Task.objects.get(pk=task_id)
    request.session['task_id'] = task_id
    return render(request, 'task_received/task_finished.html', context={'task': task})



def comment(request):
    task = Task.objects.get(pk=request.session.get('task_id'))
    if request.method == 'GET':
        return render(request, 'task_received/task_finished.html', context={'task': task})
    else:
        username = request.session.get('username')
        user = User.objects.get(username=username)
        task.is_finished = True
        user.rank += 1
        task.comment_for_publisher = request.POST.get('comment')
        task.save()
        return render(request, 'task_received/comment_or_revoke_successfuly.html',
                      context={'task': task, 'comment': 1, 'revoke': 0})


def task_sometype(request, tasktype_id):
    task_types = TaskType.objects.all()
    user_id = request.session.get('user_id')
    tasktype = TaskType.objects.get(pk=tasktype_id)
    if user_id:
        tasklist_sometype = Task.objects.filter(task_type=tasktype, hunter_id=user_id)
        paginator = Paginator(tasklist_sometype, 5)  # Show 5 contacts per page
        page = request.GET.get('page')
        try:
            tasklist_sometype = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            tasklist_sometype = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            tasklist_sometype = paginator.page(paginator.num_pages)
        return render(request, 'task_received/tasks_sometype.html',
                      context={
                          'tasklist_sometype': tasklist_sometype,
                          'task_types': task_types,
                          'typeid_now': tasktype_id
                      }
                      )
    else:
        tasklist_sometype = Task.objects.filter(task_type=tasktype, hunter_id=user_id)
        return render(request, 'task_received/tasks_sometype.html',
               context={
                   'tasklist_sometype': tasklist_sometype,
                   'task_types': task_types,
                   'typeid_now': tasktype_id,
               }
               )


def task_sometype_finished(request, tasktype_id):
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    user = User.objects.get(username=username)
    tasktype = TaskType.objects.get(pk=tasktype_id)
    task_types = TaskType.objects.all()
    tasklist_sometype_finished = Task.objects.filter(task_type=tasktype, is_finished=True, hunter_id=user_id)
    paginator = Paginator(tasklist_sometype_finished, 5)  # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        tasklist_sometype_finished = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tasklist_sometype_finished = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tasklist_sometype_finished = paginator.page(paginator.num_pages)
    return render(request, 'task_received/task_sometype_finished.html',
                  context={'tasklist_sometype_finished': tasklist_sometype_finished,
                           'task_types': task_types,
                           'typeid_now': tasktype_id})


def task_sometype_not_finished(request, tasktype_id):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    user = User.objects.get(username=username)
    tasktype = TaskType.objects.get(pk=tasktype_id)
    task_types = TaskType.objects.all()
    # = Task.objects.filter(hunter_id=username,),这里还没有登录，先改成下面这种
    # tasklist_sometype_not_finished = Task.objects.filter(task_type=tasktype, is_finished=False)

    tasklist_sometype_not_finished = Task.objects.filter(task_type=tasktype, is_finished=False, hunter_id=user_id)
    paginator = Paginator(tasklist_sometype_not_finished, 5)  # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        tasklist_sometype_not_finished = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tasklist_sometype_not_finished = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tasklist_sometype_not_finished = paginator.page(paginator.num_pages)
    return render(request, 'task_received/task_sometype_not_finished.html',
                  context={'tasklist_sometype_not_finished': tasklist_sometype_not_finished,
                           'task_types': task_types,
                           'typeid_now': tasktype_id})


def received_tasks_finished(request):
    user_id = request.session.get('user_id')
    task_types = TaskType.objects.all()
    if user_id:
        taskslist_received_finished = Task.objects.filter(is_finished=True, hunter_id=user_id)
        paginator = Paginator(taskslist_received_finished, 5)  # Show 5 contacts per page
        page = request.GET.get('page')
        try:
            taskslist_received_finished = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            taskslist_received_finished = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            taskslist_received_finished = paginator.page(paginator.num_pages)
        context = {
            'task_types': task_types,
            'taskslist_received_finished': taskslist_received_finished,
        }
        return render(request, 'task_received/received_tasks_finished.html', context)
    else:
        taskslist_received_finished = Task.objects.filter(is_finished=True)
        context = {
            'task_types': task_types,
            'taskslist_received_finished': taskslist_received_finished,
        }
        return render(request, 'task_received/received_tasks_finished.html', context)


def received_tasks_not_finished(request):
    user_id = request.session.get('user_id')
    task_types = TaskType.objects.all()
    if user_id:
        taskslist_received_not_finished = Task.objects.filter(is_finished=False, hunter_id=user_id)
        paginator = Paginator(taskslist_received_not_finished, 5)  # Show 5 contacts per page
        page = request.GET.get('page')
        try:
            taskslist_received_not_finished = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            taskslist_received_not_finished = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            taskslist_received_not_finished = paginator.page(paginator.num_pages)
        context = {
            'task_types': task_types,
            'taskslist_received_not_finished': taskslist_received_not_finished,
        }
        return render(request, 'task_received/received_tasks_not_finished.html', context)
    else: # 单元测试所用
        taskslist_received_not_finished = Task.objects.filter(is_finished=False)
        context = {
            'task_types': task_types,
            'taskslist_received_not_finished': taskslist_received_not_finished,
        }
        return render(request, 'task_received/received_tasks_not_finished.html', context)


# 退出登录
def logout(request):
    request.session['username'] = None
    request.session['user_id'] = None
    return HttpResponseRedirect(reverse('task_square'))


@csrf_exempt
def acp(request):
    if request.method == 'GET':
        id2 = request.session['mclass']
        id1 = request.session['user_id']
        user = User.objects.get(pk=id1)
        missions = Task.objects.filter(publisher_id=user)
        paginator = Paginator(missions,12,3)
        try:
            num = request.GET.get('acp', '1')
            number = paginator.page(num)
        except PageNotAnInteger:
            number = paginator.page(1)
        except EmptyPage:
            number = paginator.page(paginator.num_pages)
        context = {
            "missions": paginator,
            "id2": id2,
            "page":number
        }
        return render(request, 'task_released/acp.html', context=context)
    elif request.method == 'POST':
        if request.POST.get('task_type') == "0":
            id2 = 0
        elif request.POST.get('task_type') == "1":
            id2 = 1
        elif request.POST.get('task_type') == "2":
            id2 = 2
        elif request.POST.get('task_type') == "3":
            id2 = 3
        elif request.POST.get('task_type') == "4":
            id2 = 4
        elif request.POST.get('task_type') == "5":
            id2 = 5
        id1 = request.session['user_id']
        request.session['mclass'] = id2
        user = User.objects.get(pk=id1)
        missions = Task.objects.filter(publisher_id=user)
        paginator = Paginator(missions, 12, 3)
        try:
            num = request.POST.get('acp', '1')
            number = paginator.page(num)
        except PageNotAnInteger:
            number = paginator.page(1)
        except EmptyPage:
            number = paginator.page(paginator.num_pages)
        context = {
            "missions": paginator,
            "id2": id2,
            "page": number
        }
        return render(request, 'task_released/acp.html', context=context)


@csrf_exempt
def finish(request):
    if request.method == 'GET':
        id2 = request.session['mclass']
        id1 = request.session['user_id']
        user = User.objects.get(pk=id1)
        missions = Task.objects.filter(publisher_id=user)
        paginator = Paginator(missions,12,3)
        try:
            num = request.GET.get('finish', '1')
            number = paginator.page(num)
        except PageNotAnInteger:
            number = paginator.page(1)
        except EmptyPage:
            number = paginator.page(paginator.num_pages)
        context = {
            "missions": paginator,
            "id2": id2,
            "page":number
        }
        return render(request, 'task_released/finish.html', context=context)
    elif request.method == 'POST':
        if request.POST.get('task_type') == "0":
            id2 = 0
        elif request.POST.get('task_type') == "1":
            id2 = 1
        elif request.POST.get('task_type') == "2":
            id2 = 2
        elif request.POST.get('task_type') == "3":
            id2 = 3
        elif request.POST.get('task_type') == "4":
            id2 = 4
        elif request.POST.get('task_type') == "5":
            id2 = 5
        id1 = request.session['user_id']
        request.session['mclass'] = id2
        user = User.objects.get(pk=id1)
        missions = Task.objects.filter(publisher_id=user)
        paginator = Paginator(missions, 12, 3)
        try:
            num = request.POST.get('finish', '1')
            number = paginator.page(num)
        except PageNotAnInteger:
            number = paginator.page(1)
        except EmptyPage:
            number = paginator.page(paginator.num_pages)
        context = {
            "missions": paginator,
            "id2": id2,
            "page": number
        }
        return render(request, 'task_released/finish.html', context=context)


@csrf_exempt
def un_acp(request):
    if request.method == 'GET':
        id2 = request.session['mclass']
        id1 = request.session['user_id']
        request.session['flag']=True
        user = User.objects.get(pk=id1)
        missions = Task.objects.filter(publisher_id=user)
        paginator = Paginator(missions,12,3)
        try:
            num = request.GET.get('un_acp', '1')
            number = paginator.page(num)
        except PageNotAnInteger:
            number = paginator.page(1)
        except EmptyPage:
            number = paginator.page(paginator.num_pages)
        context = {
            "missions": paginator,
            "id2": id2,
            "page":number
        }
        return render(request, 'task_released/un_acp.html', context=context)
    elif request.method == 'POST':
        if request.POST.get('task_type') == "0":
            id2 = 0
        elif request.POST.get('task_type') == "1":
            id2 = 1
        elif request.POST.get('task_type') == "2":
            id2 = 2
        elif request.POST.get('task_type') == "3":
            id2 = 3
        elif request.POST.get('task_type') == "4":
            id2 = 4
        elif request.POST.get('task_type') == "5":
            id2 = 5
        id1 = request.session['user_id']
        request.session['mclass'] = id2
        user = User.objects.get(pk=id1)
        missions = Task.objects.filter(publisher_id=user)
        paginator = Paginator(missions, 12, 3)
        try:
            num = request.POST.get('un_acp', '1')
            number = paginator.page(num)
        except PageNotAnInteger:
            number = paginator.page(1)
        except EmptyPage:
            number = paginator.page(paginator.num_pages)
        context = {
            "missions": paginator,
            "id2": id2,
            "page": number
        }
        return render(request, 'task_released/un_acp.html', context=context)


def f_mission(request):

    id1 = request.GET.get("id")
    mission = Task.objects.get(pk=id1)
    mission.is_finished = True
    mission.save()
    request.session['id'] = id1

    return redirect("/comment")


@csrf_exempt
def comment(request):
    if request.method == 'GET':
        return render(request, 'task_released/comment.html')
    elif request.method == 'POST':
        comment1 = request.POST.get('comment')
        id1 = request.session.get("id")
        task = Task.objects.get(pk=id1)
        task.comment_for_hunter=comment1
        task.save()
        return render(request, 'task_released/success.html')


def d_mission(request):
    id1 = request.GET.get("id")
    task = Task.objects.get(pk=id1)
    task.is_pickedup = False
    request.session['hunter'] = task.hunter_id
    task.hunter = None
    task.save()
    request.session['id'] = id1
    return redirect("/reason")



@csrf_exempt
def reason(request):

    if request.method == 'GET':
        return render(request, 'task_released/reason.html')
    elif request.method == 'POST':
        reason = request.POST.get('reason')
        id1 = request.session['id']
        hunter = request.session['hunter']
        cancel = Cancel_reason()
        cancel.cancel_reason = reason
        cancel.task = Task.objects.get(pk=id1)
        cancel.user = User.objects.get(pk=hunter)
        cancel.save()
        return render(request, 'task_released/success.html')


def d_unacpm(request):
    b = request.session['flag']
    b = bool(1-b)
    request.session['flag'] = b
    if not b:
        id1 = request.GET.get("id")
        request.session['id'] = id1
        return render(request,'task_released/ensure.html')
    elif b:
        id1 = request.session['id']
        mission = Task.objects.get(pk=id1)
        mission.delete()
        return redirect("/un_acp")


def m_detail(request):
    id1 = request.GET.get("id")
    mission = Task.objects.get(pk=id1)
    type = mission.task_type.typename
    context = {
        "mission": mission,
        "type": type
    }
    return render(request, 'task_released/m_detail.html', context=context)


@csrf_exempt
def m_change(request):
    id1 = request.GET.get("id")
    request.session['id'] = id1
    mission = Task.objects.get(pk=id1)
    type = mission.task_type.typename
    context = {
        "mission": mission,
        "type": type
    }
    return render(request, 'task_released/m_change.html', context=context)


@csrf_exempt
def change_one(request):
    if request.method == 'GET':
        mdl = request.GET.get("mdl")
        id1 = request.session['id']
        mission = Task.objects.get(pk=id1)
        type = mission.task_type.typename
        context = {
            "mission": mission,
            "type": type,
            "mdl": mdl
        }
        return render(request, 'task_released/change_one.html', context=context)
    elif request.method == 'POST':
        id1 = request.session['id']
        Data = request.POST.get('Data')
        m1 = request.POST.get('m1')
        l = request.POST.get('task_type')
        c = request.POST.get('task_contact')
        z = 0
        if c == "0":
            z = 1
        elif c == "1":
            z = 2
        elif c == "2":
            z = 3
        elif c == "3":
            z = 4
        elif c == "4":
            z = 5
        d = request.POST.get('task_sketch')
        g = request.POST.get('g')
        file = request.FILES.get('task_file')
        if file is not None:
            destination = open(os.path.join(settings.BASE_DIR,'static','uploads',file.name),'wb+')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
        mission = Task.objects.get(pk=id1)
        if l is not None:
            type = TaskType.objects.get(pk=l)
            mission.task_type = type
        if Data is not None:
            mission.ddltime = Data
        if m1 is not None:
            mission.task_name = m1
        if d is not None:
            mission.task_sketch = d
        if g is not None:
            mission.task_reward = g
        if file is not None:
            mission.task_file = file.name
        if z != 0:
            mission.contact_type_publisher = Contact.objects.get(pk=z)
        mission.save()
        return redirect("/un_acp")


def download(request):
    name = request.GET.get("name")
    file = open(os.path.join(settings.BASE_DIR,'static','uploads',name),'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename ='+name.encode('utf-8').decode('ISO-8859-1')
    return response



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
        return render(request, 'tasks_square/task_square.html', context=data)

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
        return render(request, 'tasks_square/task_square.html', context=data)


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
        sort = '全部任务'
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
    return render(request, 'tasks_square/task_square.html', context=data)


def check_hunt(request, task_id):
    user_id = request.session.get('user_id')
    task = Task.objects.get(pk=task_id)
    if user_id:
        return render(request, 'tasks_square/check_hunt.html', context={'task': task,
                                                                        'user_id': user_id})
    else:
        return render(request, 'tasks_square/check_hunt.html', context={'task': task,
                                                                        'user_id': None})


def hunt_task(request, task_id):
    user_id = request.session.get('user_id')
    user = User.objects.get(pk=user_id)
    contactid = request.POST.get('contacthunter')
    contactname = Contact.objects.get(pk=contactid).typename
    task = Task.objects.get(pk=task_id)
    task.is_pickedup = True
    task.hunter_id = user_id
    task.contact_type_hunter_id = contactid
    if getattr(user, contactname) == None:
        return render(request, 'tasks_square/contacttype.html', context={'task': task,
                                                                         'contactname': contactname, })
    else:
        task.save()
        return render(request, 'tasks_square/hunt_successfully.html', context={'task': task, })


def task_details(request, task_id):
    task = Task.objects.get(pk=task_id)
    user_id = request.session.get('user_id')
    if user_id:
        data = {
            'task': task,
            'user_id': user_id,
        }
    else:
        data = {
            'task': task,
            'user_id': None,
        }
    return render(request, 'tasks_square/task_detail.html', data)


def publisher_detail(request, publisher_id):
    publisher = User.objects.get(pk=publisher_id)
    his_alltasks = publisher.publisher.all()
    his_finished = publisher.hunter.all()
    return render(request, 'tasks_square/publisher_detail.html',
                  context={'publisher': publisher,
                           'his_alltasks': his_alltasks,
                           'his_finished': his_finished})

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
        return render(request, 'tasks_square/task_square.html', context=data)
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
        return render(request, 'tasks_square/task_square.html', context=data)

@csrf_exempt
def discuss(request, task_id):
    user_id = request.session.get('user_id')
    user = User.objects.get(pk=user_id)
    task = Task.objects.get(pk=task_id)
    discussion = Discuss()
    discussion.task = task
    discussion.discuss = request.POST.get('discussion')
    discussion.discussant = user
    discussion.save()
    return HttpResponseRedirect(reverse('tasks_square:task_detail', args=[task_id]))


def response(request, task_id, discussion_id):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(pk=user_id)
        task = Task.objects.get(pk=task_id)
        discussion1 = Discuss.objects.get(pk=discussion_id)
        response1 = Response()
        response1.discuss = discussion1
        response1.response = request.POST.get('response')
        response1.respondent = user
        response1.save()
        return HttpResponseRedirect(reverse('tasks_square:task_detail', args=[task_id]))
    else:
        return render(request, 'tasks_square/task_detail.html')


def delete(request, id, type, task_id):
    if type == 'discuss':
        Discuss.objects.get(pk=id).delete()
    elif type == 'response':
        Response.objects.get(pk=id).delete()
    return HttpResponseRedirect(reverse('tasks_square:task_detail', args=[task_id]))


def downloadnew(request, task_id):
    task = Task.objects.get(pk=task_id)
    site = 'static/uploads/'
    name = str(task.task_file)
    site = site + name
    file = open(site, 'rb')
    download_name = name.split("/")[4]
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename=' + download_name.encode('utf-8').decode('ISO-8859-1')
    return response





