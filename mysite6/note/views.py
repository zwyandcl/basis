from django.shortcuts import render
from django.http import HttpResponseRedirect
from  django.http import HttpResponse
from user.models import User
from . import  models
# Create your views here.

def check_login(fn):
    def wrap(request,*args,**kwargs):
        if not hasattr(request, 'session'):  # 没有登录 hasattr判断函数有没有什么属性
            return HttpResponseRedirect('/user/login')
        if 'user' not in request.session:  # 没有登录
            return HttpResponseRedirect('/user/login')
        return fn(request,*args,**kwargs)
    return wrap


@check_login
def list_view(request):
    # 此时一定是已经登录了
    user_id = request.session['user']['id']
    # 根据已登录的用户id,找到当前登录的用户
    auser = User.objects.get(id=user_id)
    notes = auser.note_set.all()
    return render(request,'note/showall.html',locals())

@check_login
def add_view(request):
    if request.method == 'GET':
        return render(request,'note/add_note.html')
    elif request.method == 'POST':
        title = request.POST.get('title','')
        content = request.POST.get('content','')
        # 得到当前用户信息
        user_id = request.session['user']['id']
        auser = User.objects.get(id=user_id)
        anote = models.Note(user=auser)
        anote.title=title
        anote.content=content
        anote.save()
        return HttpResponseRedirect('/note/')

@check_login
def mod_view(request,id):
    user_id = request.session['user']['id']
    auser = User.objects.get(id=user_id)
    anote = models.Note.objects.get(user=auser,id=id)
    if request.method == 'GET':
        return render(request,'note/mod_note.html',locals())
    elif request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        anote.title = title
        anote.content = content
        anote.save()
        return HttpResponseRedirect('/note/')

@check_login
def del_view(request,id):
    user_id = request.session['user']['id']
    auser = User.objects.get(id=user_id)
    anote = models.Note.objects.get(user=auser, id=id)
    anote.delete()
    return HttpResponseRedirect('/note/')