from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


@never_cache
def admin_login(request):
    if 'username' in request.session:
        return redirect('admin_home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_obj = User.objects.filter(username=username)
        if not user_obj.exists():
            return render(request, 'admin_login.html')
        user_obj = authenticate(username=username, password=password)

        if user_obj and user_obj.is_superuser:
            request.session["username"] = username
            return redirect('admin_home')
        else:
            return render(request, 'admin_login.html')

    else:
        return render(request, 'admin_login.html')


@never_cache
def index(request):
    if 'username' in request.session:
        return render(request, 'admin.html')
    else:
        return redirect('admin_login')


@never_cache
def logout(request):
    if 'username' in request.session:
        print(request.session['username'])
        del request.session['username']
    return redirect('admin_login')


@never_cache
def show_users(request):
    # show all users in a table
    if 'username' in request.session:
        users = User.objects.all()
        return render(request, 'Users.html', {"users": users})
    else:
        return redirect('admin_login')


@never_cache
def edit_user(request, id):
    # edit user in database
    if 'username' in request.session:
        user = User.objects.get(id=id)
        if request.method == "POST":
            user_data = User.objects.filter(id=id).all()
            user_name = request.POST['username']
            email = request.POST['email']
            # password1=request.POST['password']
            # eny_password=pbkdf2_sha256.encrypt(password1,rounds=12000,salt_size=32)
            for user in user_data:
                user.email = email
                user.username = user_name
                # if len(password1)<12:
                #     user.password = eny_password
                user.save()
            return redirect('user_admin_home')
        else:
            return render(request, 'edit_user_form.html', {'user': user})
    else:
        return redirect('admin_login')


@never_cache
def delete_user(request, id):
    # delete user in database
    if 'username' in request.session:
        the_user = User.objects.filter(id=id).all()
        the_user.delete()
        return redirect('user_admin_home')
    else:
        return redirect('admin_login')


def searched_user(request):
    # for searching user in database
    if request.method == 'POST':
        data = request.POST['searched_data']
        user_data = User.objects.filter(username__contains=data).all()
        if user_data:
            return render(request, 'user_searched_data.html', {'user_data': user_data, 'data1': data})
        else:
            msg = "No data found"
            return render(request, 'user_searched_data.html', {'m': msg})