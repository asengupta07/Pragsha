from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(request, 'land/home.html')

def faq(request):
    return render(request, 'land/faq.html')