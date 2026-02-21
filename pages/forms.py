from django import forms

class ContactForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Your email address'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Add your feedback or questions'}), label='')
    subject = forms.CharField(widget=forms.HiddenInput(attrs={'value':'Gamer Journey Contact Form Message'}))
