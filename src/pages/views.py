from django.shortcuts import render

# Create your views here.

def index_view(request):
    context = {}
    return render(request, "index.html", context)

def credits_view(request):
    context = {}
    return render(request, "credits.html", context)

def about_view(request):
    context = {}
    return render(request, "about.html", context)
