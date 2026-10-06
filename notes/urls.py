from django.urls import path

from . import views

urlpatterns = [
    path('', views.notebook_list, name='notebook_list'),
    path('notebooks/new/', views.notebook_create, name='notebook_create'),
    path('notebooks/<int:pk>/', views.notebook_detail, name='notebook_detail'),
    path('notebooks/<int:pk>/delete/', views.notebook_delete, name='notebook_delete'),
    path('notebooks/<int:notebook_pk>/notes/new/', views.note_create, name='note_create'),
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
    path('notes/<int:pk>/edit/', views.note_update, name='note_update'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
]
