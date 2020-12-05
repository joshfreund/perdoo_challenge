from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import RequestForm
from .models import Call
from .tasks import update_model
from datetime import datetime
from django.urls import reverse


@login_required
def requests(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            req_date = form.cleaned_data['req_date']
            req = Call(
                user = request.user.id,
                url = url,
                req_date = req_date,
            )
            req.save()

            date_time_obj = datetime.strptime(req_date, '%d-%m-%Y %H:%M')
            update_model.apply_async((url, req.id), eta=date_time_obj)
            return HttpResponseRedirect(reverse('history'))
        else:
            return render(request, 'requests/requests.html', context = {'form': form})
    else:
        return render(request, 'requests/requests.html', context={'form':RequestForm()})