from django.urls.conf import path

from scan.views import ResultView, UploadView


app_name = 'scan'

urlpatterns = [
    path('', UploadView.as_view(), name='upload'),
    path('result/<int:pk>/', ResultView.as_view(), name='result')
]
