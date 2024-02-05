from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('', views.natal_chart_page, name='natal_chart'),
    path('api/chart-data/', views.get_chart_data, name='chart-data'),
    
]

urlpatterns += staticfiles_urlpatterns()