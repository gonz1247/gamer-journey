from django.shortcuts import render
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

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

def contact_view(request):
    feedback_message = None
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = f'Message from {form.cleaned_data['email']}\n'
            message += '-'*30 + '\n\n'
            message += form.cleaned_data['message']
            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email]
            success = send_mail(form.cleaned_data['subject'], message, from_email, to_email) #, fail_silently=False)
            if success:
                feedback_message = 'Successfully submitted contact form. Thank you for your feedback!'
            else:
                feedback_message = 'Contact form was not able to be submitted.'
    form = ContactForm()
    context = {'form':form,
               'feedback_message': feedback_message}
    return render(request, "contact.html", context)
