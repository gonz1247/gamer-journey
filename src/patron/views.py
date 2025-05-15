#from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import PatronRegisterForm

def register_view(request):
    if request.method == "POST":
        form = PatronRegisterForm(request.POST)
        if form.is_valid():
            patron = form.save()
            login(request, patron)
            return redirect("/")
        else:
            print('Did not create a user')
            # TODO: Add some sort of error message for invalid attempt to create user/patron
    form = PatronRegisterForm()
    context = {
        'form': form
    }
    return render(request, "patron/register.html", context)