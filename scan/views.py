import torch
import torchvision
import torchvision.transforms.functional as fn

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, DetailView

from cnn.model import CNN

from scan.forms import UploadForm
from scan.models import Uploads


# Create your views here.
class UploadView(LoginRequiredMixin, CreateView):
    """Upload Image"""

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


def recognize_character(filename: str):
    """ Character Recognition Function"""

    model_file = settings.BASE_DIR / 'cnn/ascii.pth'

    recognizer = CNN()
    recognizer.load_state_dict(torch.load(model_file))
    recognizer.eval()

    img = torchvision.io.read_image(
        filename, mode=torchvision.io.ImageReadMode.RGB
    )
    print(f"Read image shape: {img.shape}")

    img = fn.resize(img, size=(28, 28), antialias=True)
    print(f"Image shape after resize: {img.shape}")

    img = img / 255.0

    predicted_y = recognizer(img)
    print(predicted_y)
    value, index = torch.max(predicted_y, 1)
    print(value, index)

    if index.item() == 26:
        character = chr(32)
        print(f"Recognized character: '{character}'")
        return character

    character = chr(97 + index.item())
    print(f"Recognized character: '{character}'")
    return character


class ResultView(DetailView):
    model = Uploads
    template_name = 'scan/result.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: str) -> HttpResponse:
        photo = self.get_object()

        image_file = str(settings.MEDIA_ROOT / photo.image.name)
        character = recognize_character(image_file)

        caption = 'space' if character == ' ' else character
        photo.caption = caption
        photo.save()

        return super().get(request, *args, **kwargs)
