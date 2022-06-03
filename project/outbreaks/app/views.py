import json
import time
import uuid

import requests
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.views import View

from app import models

'''

开发团队：应用软件课程设计小组
开发人员：张鹏
基础处理类，其他处理继承这个类

'''


class BaseView(View):
    """
    检查指定的参数是否存在
    存在返回 True
    不存在返回 False
    """

    def isExit(param):

        if (param == None) or (param == ''):
            return False
        else:
            return True

    '''
    转换分页查询信息
    '''

    def parasePage(pageIndex, pageSize, pageTotal, count, data):

        return {'pageIndex': pageIndex, 'pageSize': pageSize, 'pageTotal': pageTotal, 'count': count, 'data': data}

    '''
    转换分页查询信息
    '''

    def parasePage(pageIndex, pageSize, pageTotal, count, data):
        return {'pageIndex': pageIndex, 'pageSize': pageSize, 'pageTotal': pageTotal, 'count': count, 'data': data}

    '''
    成功响应信息
    '''

    def success(msg='处理成功'):
        resl = {'code': 0, 'msg': msg}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    '''
    成功响应信息, 携带数据
    '''

    def successData(data, msg='处理成功'):
        resl = {'code': 0, 'msg': msg, 'data': data}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    '''
    系统警告信息
    '''

    def warn(msg='操作异常，请重试'):
        resl = {'code': 1, 'msg': msg}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    '''
    系统异常信息
    '''

    def error(msg='系统异常'):
        resl = {'code': 2, 'msg': msg}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')


'''
系统处理
用户登录等操作
'''


class SysView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'info':
            return SysView.getSessionInfo(request)
        elif module == 'checkPwd':
            return SysView.checkPwd(request)
        elif module == 'exit':
            return SysView.exit(request)
        elif module == 'notices':
            return SysView.getNoticeList(request)
        elif module == 'toptotal':
            return SysView.getTopTotal(request)
        elif module == 'nowtotal':
            return SysView.getNowTotal(request)
        elif module == 'now':
            return SysView.getTopNow(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'info':
            return SysView.updSessionInfo(request)
        elif module == 'pwd':
            return SysView.updSessionPwd(request)
        elif module == 'login':
            return SysView.login(request)
        else:
            return BaseView.error()

    '''
    用户登陆处理
    '''

    def login(request):

        userName = request.POST.get('userName')
        passWord = request.POST.get('passWord')

        user = models.Users.objects.filter(userName=userName)

        if (user.exists()):

            user = user.first()
            if user.passWord == passWord:

                token = uuid.uuid4()

                login_user = {
                    'id': user.id,
                    'userName': user.userName,
                    'passWord': user.passWord,
                    'name': user.name,
                    'age': user.age,
                    'gender': user.gender,
                    'type': user.type,
                }

                resl = {
                    'token': str(token)
                }

                cache.set(token, login_user, 60 * 60 * 60 * 3)

                return SysView.successData(resl)
            else:
                return SysView.error('用户密码输入错误')
        else:
            return SysView.error('用户名输入错误')

    '''
    用户登出处理
    '''

    def exit(request):

        token = request.GET.get('token')

        cache.delete(token)

        return BaseView.success()

    def checkPwd(request):

        token = request.GET.get('token')
        oldPwd = request.GET.get('oldPwd')

        loginUser = cache.get(token)

        if (loginUser['passWord'] == oldPwd):
            return BaseView.success()
        else:
            return BaseView.warn('原始密码输入错误')

    '''
    获取登陆用户信息
    '''

    def getSessionInfo(request):

        token = request.GET.get('token')

        return BaseView.successData(cache.get(token))

    '''
    修改登陆用户信息
    '''

    def updSessionInfo(request):

        token = request.POST.get('token')
        loginUser = cache.get(token)

        print(loginUser)

        models.Users.objects. \
            filter(id=loginUser['id']).update(
            userName=request.POST.get('userName'),
            name=request.POST.get('name'),
            gender=request.POST.get('gender'),
            age=request.POST.get('age'),
        )

        return BaseView.success()

    '''
    修改登陆用户密码
    '''

    def updSessionPwd(request):

        token = request.POST.get('token')
        loginUser = cache.get(token)

        models.Users.objects. \
            filter(id=loginUser['id']).update(
            passWord=request.POST.get('newPwd'),
        )

        return BaseView.success()

    '''
    获取当前统计信息
    '''

    def getTopNow(request):

        data = models.Statistics.objects.all().order_by('-createTime').first()

        resl = {
            'date': data.createTime,
            'confirm': data.confirm,
            'dead': data.dead,
            'heal': data.heal,
            'nowConfirm': data.nowConfirm
        }

        return BaseView.successData(resl)

    '''
    获取前7日统计信息
    '''

    def getTopTotal(request):

        resl = []

        dataLogs = models.Statistics.objects.all().order_by('-createTime')[:7]

        for item in dataLogs:
            temp = {
                'date': item.createTime,
                'confirm': item.confirm,
                'dead': item.dead,
                'heal': item.heal,
            }
            resl.append(temp)

        return BaseView.successData(resl)

    '''
    获取近7天每日确证
    '''

    def getNowTotal(request):

        resl = []

        dataLogs = models.Statistics.objects.all().order_by('-createTime')[:7]

        for item in dataLogs:
            temp = {
                'date': item.createTime,
                'nowConfirm': item.nowConfirm,
            }
            resl.append(temp)

        return BaseView.successData(resl)

    '''
    获取前通知信息
    '''

    def getNoticeList(request):
        resl = []

        dataLogs = models.Notices.objects.all().order_by('-createTime')

        for item in dataLogs:
            temp = {
                'id': item.id,
                'title': item.title,
                'detail': item.detail,
                'createTime': item.createTime,
            }
            resl.append(temp)

        return BaseView.successData(resl)


'''
统计数据
'''


class StatisticsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        return StatisticsView.getPageInfo(request)

    def post(self, request, module, *args, **kwargs):

        return StatisticsView.initData(request)

    '''
    初始化数据
    '''

    def initData(request):

        models.Statistics.objects.all().delete()

        url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,cityStatis,provinceCompare'

        resp = requests.get(url)

        data = resp.json()

        resp = (data['data'])['chinaDayList']

        for item in resp:
            tempDates = str(item['date']).split('.')

            models.Statistics.objects.create(
                createTime=f'{item["y"]}-{tempDates[0]}-{tempDates[1]}',
                confirm=item['confirm'],
                dead=item['dead'],
                heal=item['heal'],
                nowConfirm=item['nowConfirm']
            )

        return BaseView.success()

    '''
    分页查看数据
    '''

    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        data = models.Statistics.objects.all().order_by('-createTime')

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'createTime': item.createTime,
                'confirm': item.confirm,
                'dead': item.dead,
                'heal': item.heal,
                'nowConfirm': item.nowConfirm,
            }
            resl.append(temp)

        temp = BaseView.parasePage(int(pageIndex), int(pageSize),
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(temp)


'''
求助通知信息处理
'''


class NoticesView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'info':
            return NoticesView.getInfo(request)
        elif module == 'page':
            return NoticesView.getPageInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'add':
            return NoticesView.addInfo(request)
        elif module == 'upd':
            return NoticesView.updInfo(request)
        elif module == 'del':
            return NoticesView.delInfo(request)
        else:
            return BaseView.error()

    '''
    获取指定数据
    '''

    def getInfo(request):

        data = models.Notices.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'title': data.title,
            'detail': data.detail,
            'createTime': data.createTime,
        }

        return BaseView.successData(resl)

    '''
    分页获取数据
    '''

    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        title = request.GET.get('title')

        qruery = Q();

        if BaseView.isExit(title):
            qruery = qruery & Q(title__contains=title)

        data = models.Notices.objects.filter(qruery)

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'title': item.title,
                'detail': item.detail,
                'createTime': item.createTime,
            }
            resl.append(temp)

        temp = BaseView.parasePage(int(pageIndex), int(pageSize),
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(temp)

    '''
    添加数据
    '''

    def addInfo(request):

        models.Notices.objects.create(
            title=request.POST.get('title'),
            detail=request.POST.get('detail'),
            createTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )

        return BaseView.success()

    '''
    修改数据
    '''

    def updInfo(request):

        models.Notices.objects. \
            filter(id=request.POST.get('id')).update(
            title=request.POST.get('title'),
            detail=request.POST.get('detail'),
        )

        return BaseView.success()

    '''
    删除数据
    '''

    def delInfo(request):

        models.Notices.objects.filter(id=request.POST.get('id')).delete()

        return BaseView.success()


'''
疫情物资处理

'''


class VaccinateLogsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'info':
            return VaccinateLogsView.getInfo(request)
        elif module == 'page':
            return VaccinateLogsView.getPageInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'add':
            return VaccinateLogsView.addInfo(request)
        elif module == 'upd':
            return VaccinateLogsView.updInfo(request)
        elif module == 'del':
            return VaccinateLogsView.delInfo(request)
        else:
            return BaseView.error()

    '''
    获取指定数据
    '''

    def getInfo(request):

        data = models.VaccinateLogs.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'name': data.name,
            'card': data.card,
            'phone': data.phone,
            'address': data.address,
            'vaccinateNo': data.vaccinateNo,
            'vaccinateTime': data.vaccinateTime,
            'uName': data.user.name,
        }
        return BaseView.successData(resl)

    '''
    分页获取数据
    '''

    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')
        card = request.GET.get('card')
        phone = request.GET.get('phone')
        address = request.GET.get('address')

        user = cache.get(request.GET.get('token'))

        qruery = Q();

        if user['type'] == 1:
            qruery = qruery & Q(user__id=user['id'])

        if BaseView.isExit(name):
            qruery = qruery & Q(name__contains=name)
        if BaseView.isExit(card):
            qruery = qruery & Q(card__contains=card)
        if BaseView.isExit(phone):
            qruery = qruery & Q(phone__contains=phone)
        if BaseView.isExit(address):
            qruery = qruery & Q(address__contains=address)

        data = models.VaccinateLogs.objects.filter(qruery)

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'name': item.name,
                'card': item.card,
                'phone': item.phone,
                'address': item.address,
                'vaccinateNo': item.vaccinateNo,
                'vaccinateTime': item.vaccinateTime,
                'uName': item.user.name,
            }
            resl.append(temp)

        temp = BaseView.parasePage(int(pageIndex), int(pageSize),
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(temp)

    '''
    添加数据
    '''

    def addInfo(request):

        user = cache.get(request.POST.get('token'))

        models.VaccinateLogs.objects.create(
            name=request.POST.get('name'),
            card=request.POST.get('card'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            vaccinateNo=request.POST.get('vaccinateNo'),
            vaccinateTime=request.POST.get('vaccinateTime'),
            user=models.Users.objects.filter(id=user['id']).first(),
        )

        return BaseView.success()

    '''
    修改数据
    '''

    def updInfo(request):

        models.VaccinateLogs.objects. \
            filter(id=request.POST.get('id')).update(
            name=request.POST.get('name'),
            card=request.POST.get('card'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            vaccinateNo=request.POST.get('vaccinateNo'),
            vaccinateTime=request.POST.get('vaccinateTime'),
        )
        return BaseView.success()

    '''
    删除数据
    '''

    def delInfo(request):

        models.VaccinateLogs.objects.filter(id=request.POST.get('id')).delete()

        return BaseView.success()


'''
出入库记录处理
'''


class CheckLogsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'info':
            return CheckLogsView.getInfo(request)
        elif module == 'page':
            return CheckLogsView.getPageInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'add':
            return CheckLogsView.addInfo(request)
        elif module == 'upd':
            return CheckLogsView.updInfo(request)
        elif module == 'del':
            return CheckLogsView.delInfo(request)
        else:
            return BaseView.error()

    '''
    获取指定数据
    '''

    def getInfo(request):

        data = models.CheckLogs.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'title': data.title,
            'detail': data.detail,
            'createTime': data.createTime,
        }

        return BaseView.successData(resl)

    '''
    分页获取数据
    '''

    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        resl = request.GET.get('resl')
        loc = request.GET.get('loc')

        user = cache.get(request.GET.get('token'))

        qruery = Q();

        if user['type'] == 1:
            qruery = qruery & Q(user__id=user['id'])

        if BaseView.isExit(resl):
            qruery = qruery & Q(resl=resl)

        if BaseView.isExit(loc):
            qruery = qruery & Q(loc__contains=loc)

        data = models.CheckLogs.objects.filter(qruery)

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'loc': item.loc,
                'resl': item.resl,
                'detail': item.detail,
                'userName': item.user.name,
                'createTime': item.createTime,
            }
            resl.append(temp)

        temp = BaseView.parasePage(int(pageIndex), int(pageSize),
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(temp)

    '''
    添加数据
    '''

    def addInfo(request):

        user = cache.get(request.POST.get('token'))

        models.CheckLogs.objects.create(
            loc=request.POST.get('loc'),
            resl=request.POST.get('resl'),
            detail=request.POST.get('detail'),
            user=models.Users.objects.filter(id=user['id']).first(),
            createTime=time.strftime("%Y-%m-%d", time.localtime())
        )

        return BaseView.success()

    '''
    修改数据
    '''

    def updInfo(request):

        models.CheckLogs.objects. \
            filter(id=request.POST.get('id')).update(
            loc=request.POST.get('loc'),
            resl=request.POST.get('resl'),
            detail=request.POST.get('detail'),
        )

        return BaseView.success()

    '''
    删除数据
    '''

    def delInfo(request):

        models.CheckLogs.objects.filter(id=request.POST.get('id')).delete()

        return BaseView.success()


'''
异常登记处理
开发人员：庞渝昊
'''


class AbnormityLogsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'info':
            return AbnormityLogsView.getInfo(request)
        elif module == 'page':
            return AbnormityLogsView.getPageInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'add':
            return AbnormityLogsView.addInfo(request)
        elif module == 'upd':
            return AbnormityLogsView.updInfo(request)
        elif module == 'del':
            return AbnormityLogsView.delInfo(request)
        else:
            return BaseView.error()

    '''
    获取指定数据
    '''

    def getInfo(request):

        data = models.AbnormityLogs.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'detail': data.detail,
            'createTime': data.createTime,
        }

        return BaseView.successData(resl)

    '''
    分页获取数据
    '''

    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')

        user = cache.get(request.GET.get('token'))

        qruery = Q();

        if user['type'] == 1:
            print(user['id'], user['type'])
            qruery = qruery & Q(user__id=user['id'])

        if BaseView.isExit(name):
            qruery = qruery & Q(user__name__contains=name)

        data = models.AbnormityLogs.objects.filter(qruery)

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'uName': item.user.name,
                'detail': item.detail,
                'createTime': item.createTime,
            }
            resl.append(temp)

        temp = BaseView.parasePage(int(pageIndex), int(pageSize),
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(temp)

    '''
    添加数据
    '''

    def addInfo(request):

        user = cache.get(request.POST.get('token'))

        models.AbnormityLogs.objects.create(
            detail=request.POST.get('detail'),
            user=models.Users.objects.filter(id=user['id']).first(),
            createTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )

        return BaseView.success()

    '''
    修改数据
    '''

    def updInfo(request):

        models.AbnormityLogs.objects. \
            filter(id=request.POST.get('id')).update(
            detail=request.POST.get('detail'),
        )

        return BaseView.success()

    '''
    删除数据
    '''

    def delInfo(request):

        models.AbnormityLogs.objects.filter(id=request.POST.get('id')).delete()

        return BaseView.success()


'''
系统用户处理

'''


class UsersView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'info':
            return UsersView.getInfo(request)
        elif module == 'page':
            return UsersView.getPageInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'add':
            return UsersView.addInfo(request)
        elif module == 'upd':
            return UsersView.updInfo(request)
        elif module == 'del':
            return UsersView.delInfo(request)
        else:
            return BaseView.error()

    '''
    获取指定数据
    '''

    def getInfo(request):

        data = models.Users.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'userName': data.userName,
            'passWord': data.passWord,
            'name': data.name,
            'gender': data.gender,
            'age': data.age,
            'phone': data.phone,
            'address': data.address,
            'type': data.type,
        }

        return BaseView.successData(resl)

    '''
    分页获取数据
    '''

    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        userName = request.GET.get('userName')
        name = request.GET.get('name')
        phone = request.GET.get('phone')

        qruery = Q();

        if BaseView.isExit(userName):
            qruery = qruery & Q(userName__contains=userName)

        if BaseView.isExit(name):
            qruery = qruery & Q(name__contains=name)

        if BaseView.isExit(phone):
            qruery = qruery & Q(phone__contains=phone)

        data = models.Users.objects.filter(qruery)

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'userName': item.userName,
                'passWord': item.passWord,
                'name': item.name,
                'gender': item.gender,
                'age': item.age,
                'phone': item.phone,
                'address': item.address,
                'type': item.type,
            }
            resl.append(temp)

        temp = BaseView.parasePage(int(pageIndex), int(pageSize),
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(temp)

    '''
    添加数据
    '''

    def addInfo(request):

        models.Users.objects.create(
            userName=request.POST.get('userName'),
            passWord=request.POST.get('passWord'),
            name=request.POST.get('name'),
            gender=request.POST.get('gender'),
            age=request.POST.get('age'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            type=request.POST.get('type'),
        )

        return BaseView.success()

    '''
    修改数据
    '''

    def updInfo(request):

        models.Users.objects. \
            filter(id=request.POST.get('id')).update(
            userName=request.POST.get('userName'),
            passWord=request.POST.get('passWord'),
            name=request.POST.get('name'),
            gender=request.POST.get('gender'),
            age=request.POST.get('age'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
        )

        return BaseView.success()

    '''
    删除数据
    '''

    def delInfo(request):

        models.Users.objects.filter(id=request.POST.get('id')).delete()

        return BaseView.success()
