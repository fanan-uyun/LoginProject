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
    v1.2 如果cookie当中的username和session当中的username不一致，认为不合法
    """
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get("username")
        # v1.2 获取session会话中“username的值
        session_user = request.session.get("username")
        # 如果cookie和session中的username都不为空
        if username and session_user:
            user = LoginUser.objects.filter(username=username).first()
            # 如果数据库中这个username存在，并且cookie和session的username一致
            if user and username == session_user:
                return fun(request,*args,**kwargs)
        return HttpResponseRedirect("/login/")
    return inner

@LoginValid
def index(request):
    return render(request,"index.html")

# v1.2将检验用户名是否存在封装成一个函数，因为此前这个功能重复太多
def userValid(username):
    """
    校验用户是否存在
    """
    user = LoginUser.objects.filter(username=username).first()
    return user

def register(request):
    result = {"content":""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            # u = LoginUser.objects.filter(username=username).first()
            u = userValid(username) #应用校验用户是否存在功能
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
            # u = LoginUser.objects.filter(username=username).first()
            u = userValid(username)  # 应用校验用户是否存在功能
            if u:  # 用户名存在
                if u.password == setPassword(password):# 密码正确
                    response = HttpResponseRedirect("/index/")
                    response.set_cookie("username",u.username)
                    # v1.2 新增session的下发
                    request.session["username"] = u.username
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



