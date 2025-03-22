from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def Dontate_Success(request):
    pass
@login_required
def Donate(request):
    pass

@login_required
def My_Donations(request):
    pass