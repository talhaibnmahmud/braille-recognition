from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, DetailView

from scan.forms import UploadForm
from scan.models import Uploads


# Create your views here.
class UploadView(LoginRequiredMixin, CreateView):
    model = Uploads
    fields = '__all__'
    # success_url = '/scan/result/{id}'
    template_name = 'scan/scan.html'

    def post(self, request: HttpRequest, *args: str, **kwargs: str) -> HttpResponse:
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.user = request.user
            form.save()

            return redirect(reverse_lazy('scan:result', kwargs={'pk': form.instance.pk}))
        return super().post(request, *args, **kwargs)


class ResultView(DetailView):
    model = Uploads
    template_name = 'scan/result.html'
