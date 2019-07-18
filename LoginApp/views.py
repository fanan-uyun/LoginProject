from django.shortcuts import render,render_to_response
from LoginApp.models import LoginUser
from django.http import HttpResponseRedirect
import hashlib
# Create your views here.
# v1.1新增密码加密功能，对注册、登录加密
def setPassword(password):
    """
    对密码进行加密
    """
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

# v1.1新增登录校验装饰器
def LoginValid(fun):
    """
    cookie校验装饰器
    """
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get("username")
        if username:
            user = LoginUser.objects.filter(username=username).first()
            if user:
                return fun(request,*args,**kwargs)
        return HttpResponseRedirect("/login/")
    return inner

@LoginValid
def index(request):
    return render(request,"index.html")


def register(request):
    result = {"content":""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            u = LoginUser.objects.filter(username=username).first()
            if u:# 用户名存在
               result["content"] = "账户已注册"
            else:
                user = LoginUser()
                user.username = username
                user.password = setPassword(password)
                user.save()
                return HttpResponseRedirect("/login/")
        else:
            result["content"] = "账户或密码不能为空"

    return render(request,"register.html",locals())

def login(request):
    result = {"content": ""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:# 如果用户和密码不为空
            u = LoginUser.objects.filter(username=username).first()
            if u:  # 用户名存在
                if u.password == setPassword(password):# 密码正确
                    response = HttpResponseRedirect("/index/")
                    response.set_cookie("username",u.username)
                    return response
                else:
                    result["content"] = "密码错误"
            else:
                result["content"] = "用户名不存在"
        else:
            result["content"] = "账户或密码不能为空"
    return render(request,"login.html",locals())

def logout(request):
    response = HttpResponseRedirect("/login/")
    response.delete_cookie("username")
    return response



