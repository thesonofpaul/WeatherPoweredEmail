from django.http import HttpResponseRedirect
from django.shortcuts import render, get_list_or_404
from django.urls import reverse
from django.views import generic

from .models import Cities, Email_List


class IndexView(generic.ListView):
    template_name = 'newsletter/index.html'
    context_object_name = 'cities'

    def get_queryset(self):
        return get_list_or_404(Cities)

# def index(request):
#     cities = get_list_or_404(Cities)
#     context = {'cities': cities}
#     return render(request, 'newsletter/index.html', context)

def submit(request):
    try:
        new_email = request.POST['email_address']
        new_location = Cities.objects.get(id=request.POST['city'])
    except (KeyError, Cities.DoesNotExist):
        return render(request, "newsletter/index.html",
                      {'cities': get_list_or_404(Cities),
                       'error_list': "Invalid selection"})
    else:
        new_entry = Email_List(email_address=new_email, location_id=new_location).save()
        return HttpResponseRedirect(reverse('result', args=(new_entry.location_id,)))

class ResultView(generic.DetailView):
    model = Email_List
    template_name = 'newsletter/result.html'

# def result(request, question_id):
#     entry = get_object_or_404(Email_List, pk=question_id)
#     return render(request, 'newsletter/result.html', {'entry': entry})