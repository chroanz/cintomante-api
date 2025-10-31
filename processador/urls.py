from django.urls import path
from .views import UploadImagemView

urlpatterns = [
    path('', UploadImagemView.as_view(), name='upload-imagem'),
]