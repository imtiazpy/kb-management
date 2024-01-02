from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse


def login_page_view(request):
    return render(request, 'users/login_page.html')


def login_view(request):
    logout()
    resp = {"status": 'failed', 'msg': ''}
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return JsonResponse(resp)


def logout_view(request):
    logout(request)
    return redirect('login')
