from django.urls import path
from .views import upload_csv, get_history, generate_pdf
from .views import login_user

urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('history/', get_history, name='history'),
    path('report/', generate_pdf, name='generate_pdf'),
    path('login/', login_user),
]