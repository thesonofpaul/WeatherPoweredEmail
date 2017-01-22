from django.http import HttpResponseRedirect
from django.shortcuts import render, get_list_or_404
from django.urls import reverse
from django.views import generic

from .models import Cities, EmailList


class IndexView(generic.ListView):
    template_name = 'newsletter/index.html'
    context_object_name = 'cities'

    def get_queryset(self):
        return get_list_or_404(Cities.objects.order_by('city'))


def submit(request):
    if request.POST['email_address'] is None or request.POST['email_address'] == "":
        return render(request, "newsletter/index.html",
                      {'cities': get_list_or_404(Cities),
                       'error_message': "Invalid selection. Please try again."})
    try:
        new_email = request.POST['email_address']
        new_location = Cities.objects.get(id=int(request.POST['city']))
    except (KeyError, ValueError, Cities.DoesNotExist):
        return render(request, "newsletter/index.html",
                      {'cities': get_list_or_404(Cities),
                       'error_message': "Invalid selection. Please try again."})
    else:
        if not EmailList.objects.filter(email_address=new_email).exists():
            new_entry = EmailList(email_address=new_email, location=new_location)
            new_entry.save()
            return HttpResponseRedirect(reverse('result', args=(new_entry.id,)))
        else:
            return render(request, "newsletter/index.html",
                          {'cities': get_list_or_404(Cities),
                           'error_message': "It looks like this email has already been used.\n"
                                            "Please try again."})


class ResultView(generic.ListView):
    template_name = 'newsletter/result.html'
    context_object_name = 'entry'

    def get_queryset(self):
        return EmailList.objects.latest('id')
