from django.shortcuts import render, get_object_or_404
from .models import Cities, Email_List


def index(request):
    cities = get_object_or_404(Cities.objects)
    context = {'cities': cities}
    return render(request, 'newsletter/index.html', context)

'''def submit(request):
    try:
        new_post = request.POST['email_address']
    except (KeyError):
        return
'''