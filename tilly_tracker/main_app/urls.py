from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name="about"),
    path('plants/', views.plants_index, name="index"),
    path('plants/<int:plant_id>/', views.plant_detail, name='detail'),
    path('plants/create/', views.PlantCreate.as_view(), name='plants_create'),
    path('plants/<int:pk>/update/',
         views.PlantUpdate.as_view(), name='plants_update'),
    path('plants/<int:pk>/delete/',
         views.PlantDelete.as_view(), name='plants_delete'),
    path('plants/<int:plant_id>/add_watering/',
         views.add_watering, name='add_watering'),
     path('plants/<int:plant_id>/assoc_vessel/<int:vessel_id>/', views.assoc_vessel, name='assoc_vessel'),
    path('vessels/', views.VesselList.as_view(), name='vessels_index'),
    path('vessels/<int:pk>/', views.VesselDetail.as_view(), name='vessels_detail'),
    path('vessels/create/', views.VesselCreate.as_view(), name='vessels_create'),
    path('vessels/<int:pk>/update/', views.VesselUpdate.as_view(), name='vessels_update'),
    path('vessels/<int:pk>/delete/', views.VesselDelete.as_view(), name='vessels_delete'),
    path('accounts/signup/', views.signup, name='signup')
]
