from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("select_dashboard")

        return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def select_dashboard(request):
    user = request.user
    if user.is_superuser:
        return redirect("admin_dashboard")
    elif hasattr(user, "role") and user.role.name == "Teacher":
        return redirect("teacher_dashboard")
    else:
        return redirect("student_dashboard")
