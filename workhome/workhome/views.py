from django.shortcuts import render
from . import models


# Create your views here.

def index(request):
    return render(request, 'index.html')


def entry_storage(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        entry_id = request.GET.getlist('entry_id')
        goods_id = request.GET.getlist('goods_id')
        storage_id = request.GET.getlist('storage_id')
        supplier_id = request.GET.getlist('supplier_id')
        goods_price = request.GET.getlist('goods_price')
        goods_num = request.GET.getlist('goods_num')
        entry_data = request.GET.getlist('entry_data')
        insert = models.entry_bill.objects.create(entry_id=entry_id[0], goods_id=goods_id[0], storage_id=storage_id[0],
                                                  supplier_id=supplier_id[0], goods_price=goods_price[0],
                                                  goods_num=goods_num[0], entry_data=entry_data[0])
        insert.save()
    entry_bill = models.entry_bill.objects.values()
    return render(request, 'entry_storage.html', {'entry_bill': entry_bill})


def entry_storage_delete(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        entry_id = request.GET.getlist('entry_id')
        deletesql = models.entry_bill.objects.filter(entry_id=entry_id[0]).delete()
    entry_bill = models.entry_bill.objects.values()
    return render(request, 'entry_storage.html', {'entry_bill': entry_bill})


def goods(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        goods_id = request.GET.getlist('goods_id')
        goods_name = request.GET.getlist('goods_name')
        goods_num = request.GET.getlist('goods_num')
        goods_sort = request.GET.getlist('goods_sort')
        goods_remark = request.GET.getlist('goods_remark')
        insert = models.goods.objects.create(goods_id=goods_id[0], goods_name=goods_name[0], goods_num=goods_num[0],
                                             goods_sort=goods_sort[0], goods_remark=goods_remark[0])
        insert.save()
    goods = models.goods.objects.values()
    return render(request, 'goods.html', {'goods': goods})


def goods_delete(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        goods_id = request.GET.getlist('goods_id')
        deletesql = models.goods.objects.filter(goods_id=goods_id[0]).delete()
    goods = models.goods.objects.values()

    return render(request, 'goods.html', {'goods': goods})


def out_storage(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        out_id = request.GET.getlist('out_id')
        goods_id = request.GET.getlist('goods_id')
        storage_id = request.GET.getlist('storage_id')
        subscriber_id = request.GET.getlist('subscriber_id')
        goods_price = request.GET.getlist('goods_price')
        goods_num = request.GET.getlist('goods_num')
        out_data = request.GET.getlist('out_data')
        insert = models.out_bill.objects.create(out_id=out_id[0], goods_id=goods_id[0], storage_id=storage_id[0],
                                                subscriber_id=subscriber_id[0], goods_price=goods_price[0],
                                                goods_num=goods_num[0], out_data=out_data[0])
        insert.save()
    out_bill = models.out_bill.objects.values()
    return render(request, 'out_storage.html', {'out_bill': out_bill})


def out_storage_delete(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        out_id = request.GET.getlist('out_id')
        deletesql = models.out_bill.objects.filter(out_id=out_id[0]).delete()
    out_bill = models.out_bill.objects.values()

    return render(request, 'out_storage.html', {'out_bill': out_bill})


def storage(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        storage_id = request.GET.getlist('storage_id')
        storage_name = request.GET.getlist('storage_name')

        insert = models.storage.objects.create(storage_id=storage_id[0], storage_name=storage_name[0])
        insert.save()
    storage = models.storage.objects.values()
    return render(request, 'storage.html', {'storage': storage})


def storage_delete(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        storage_id = request.GET.getlist('storage_id')
        deletesql = models.v.objects.filter(storage_id=storage_id[0]).delete()
    storage = models.storage.objects.values()

    return render(request, 'storage.html', {'subscriber': storage})


def subscriber(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        subscriber_id = request.GET.getlist('subscriber_id')
        subscriber_name = request.GET.getlist('subscriber_name')

        insert = models.subscriber.objects.create(subscriber_id=subscriber_id[0], subscriber_name=subscriber_name[0])
        insert.save()
    subscriber = models.subscriber.objects.values()
    return render(request, 'subscriber.html', {'subscriber': subscriber})


def subscriber_delete(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        subscriber_id = request.GET.getlist('subscriber_id')
        deletesql = models.subscriber.objects.filter(subscriber_id=subscriber_id[0]).delete()
    subscriber = models.subscriber.objects.values()

    return render(request, 'subscriber.html', {'subscriber': subscriber})


def supplier(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        supplier_id = request.GET.getlist('supplier_id')
        supplier_name = request.GET.getlist('supplier_name')

        insert = models.supplier.objects.create(supplier_id=supplier_id[0], supplier_name=supplier_name[0])
        insert.save()
    supplier = models.supplier.objects.values()
    return render(request, 'supplier.html', {'supplier': supplier})


def supplier_delete(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        supplier_id = request.GET.getlist('supplier_id')
        deletesql = models.supplier.objects.filter(supplier_id=supplier_id[0]).delete()
    supplier = models.supplier.objects.values()

    return render(request, 'supplier.html', {'supplier': supplier})
