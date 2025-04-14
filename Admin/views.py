from django.shortcuts import render
from django.contrib.auth.decorators import login_required ,user_passes_test
# Create your views here.
from Authentication.models import User
from Word.models import *

def admin_required(user):
    return user.is_superuser


"""

Admin Dashboard

"""
@user_passes_test(admin_required)
@login_required
def AdminDashboard(request):
    total_words = Words.objects.all().count()
    total_users = User.objects.all().count()
    context = {
        "total_words":total_words,
        "total_users":total_users,
    }
    return render(request, 'Admin/Home.html', context)

@user_passes_test(admin_required)
@login_required
def ConfirmWords(request):
    pass

@user_passes_test(admin_required)
@login_required
def AllWords(request):
    pass

@user_passes_test(admin_required)
@login_required
def NoWords(request):
    pass

@user_passes_test(admin_required)
@login_required
def AllUsers(request):
    pass

@user_passes_test(admin_required)
@login_required
def DeleteWord(request,word_id):
    pass

@user_passes_test(admin_required)
@login_required
def DeleteUser(request,user_id):
    pass

@user_passes_test(admin_required)
@login_required
def EditWord(request,word_id):
    pass

@user_passes_test(admin_required)
@login_required
def EditUser(request,user_id):
    pass

@user_passes_test(admin_required)
@login_required
def AddWord(request):
    pass

@user_passes_test(admin_required)
@login_required
def AllDonate(request):
    pass

@user_passes_test(admin_required)
@login_required
def Donate(request,donate_id):
    pass

