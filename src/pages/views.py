from django.shortcuts import render

# Create your views here.

def index_view(request):
    context = {}
    # TODO: Add logic for logged in users to get page with options, if not get generic welcome page
    context = {'patron':'Gonzo'}
    return render(request, "index.html", context)

def credits_view(request):
    context = {}
    return render(request, "credits.html", context)
