from django.shortcuts import render
from django.shortcuts import render

def index(request):
    return render(request, 'user/index.html')

def reports(request):
    return render(request, 'user/reports.html')
