from django.contrib import admin
from django.urls import path, include
from cone_dashboard import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('results/', views.training_results , name='training_results'),
    path('testing/', views.testing,name='testing'),
    path('api/metrics/', views.metrics_data, name='metrics_data'),
    path('api/co2-Yolo12/', views.co2_data_Yolo12, name='co2-Yolo12'),
    path('api/co2-Faster/', views.co2_data_Faster, name='co2-Faster'),
    path('api/yolo-images/', views.yolo_images, name='yolo-images'),
    path('api/faster-images/', views.faster_images, name='faster-images'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)