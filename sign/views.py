from django.shortcuts import render_to_response
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import render
from sign.models import Event,Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
import json
# Create your views here.



def index(request):
    print ("test")
    return render(request,'index.html')



def login_action(request):
    if request.method == 'POST':
        p_username = request.POST.get('username', '')
        p_password = request.POST.get('password', '')

        if p_username == '' or p_password == '':
            return render(request,'index.html',{"error":"username or password is null"})

        user = auth.authenticate(username=p_username, password=p_password)

        if user is not None:
            auth.login(request, user)
            request.session['username'] = p_username
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render_to_response('index.html', {'error': "username or password incorrect"})
    else:
        return HttpResponse("not post!")


def logout(request):

    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response


def event_manage(request):
    event_list = Event.objects.all()
    usersession = request.session.get('username','')
    return render(request,'event_manage.html',{"user":usersession,"events":event_list})

def search_name(request):
    usersession = request.session.get('username', '')
    search_name = request.GET.get('name', '')
    search_name_bytes = search_name.encode(encoding="utf-8")
    event_list = Event.objects.filter(name__contains=search_name_bytes)
    return render(request, "event_manage.html", {"user": usersession, "events": event_list})


def guest_manage(request):
    guest_list = Guest.objects.all()
    usersession = request.session.get('username', '')
    return render(request,'guest_manage.html',{"user":usersession,"guests":guest_list})

def search_phone(request):

    '''
        usersession = request.session.get('username', '')
        search_phone = request.GET.get('phone', '')
        guest_list = Guest.objects.filter(name__contains=search_phone)
        return render(request, 'guest_manage.html', {"user": usersession, "guests": guest_list})
    '''

    search_phone = request.GET.get("phone", "")
    guest_list = Guest.objects.filter(phone__contains=search_phone)
    username = request.session.get('username', '')

    paginator = Paginator(guest_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:

        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {"user": username, "guests": contacts})

# 签到页面
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)           # 签到人数
    sign_list = Guest.objects.filter(sign="1", event_id=event_id)   # 已签到数
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list))
    return render(request, 'sign_index.html', {'event': event,
                                               'guest':guest_data,
                                               'sign':sign_data})

def sign_index_action(request,event_id):

    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)
    sign_list = Guest.objects.filter(sign="1", event_id=event_id)
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list)+1)

    phone =  request.POST.get('phone','')

    result = Guest.objects.filter(phone = phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': '手机号为空或不存在','guest':guest_data,'sign':sign_data})

    result = Guest.objects.filter(phone = phone,event_id = event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': '该用户未参加此次发布会','guest':guest_data,'sign':sign_data})

    result = Guest.objects.get(phone = phone)

    if result.sign:
        return render(request, 'sign_index.html', {'event': event,'hint': "已签到",'guest':guest_data,'sign':sign_data})
    else:
        Guest.objects.filter(phone = phone).update(sign = '1')
        return render(request, 'sign_index.html', {'event': event,'hint':'签到成功!','user': result,'guest':guest_data,'sign':sign_data})

def add_event(request):
    eid = request.POST.get('eid','')
    name = request.POST.get('name','')
    status = request.POST.get('status','')
    limit = request.POST.get('limit', '')
    starttime = request.POST.get('start_time', '')
    address = request.POST.get('address', '')

    if eid == '' or name == '' or starttime == '' or address == '':
        return HttpResponse('parameter error')
    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({"status":10022,"message":"evevt_id already exist"})
    if status == '':
        status =1

    Event.objects.create(id=eid, name=name, status=status, limit=limit, starttime=starttime, address=address)
    return JsonResponse({"status":200, "message":"add event success"})