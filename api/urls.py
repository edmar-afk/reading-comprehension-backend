from django.urls import path
from . import views

urlpatterns = [
    
    # List all reading materials
    path('reading-materials/',views.ReadingMaterialsListCreateView.as_view(),name='reading-materials-list-create'),
    path("reading-materials/<int:pk>/",views.ReadingMaterialsDetailView.as_view(),name="reading-materials-detail",),
    path('reading-materials/add/',views.ReadingMaterialsListCreateView.as_view(),name='reading-materials-add'),
    path('reading-materials/edit/<int:pk>/',views.ReadingMaterialsDetailView.as_view(),name='reading-materials-edit'),
    path('reading-materials/delete/<int:pk>/',views.ReadingMaterialsDetailView.as_view(),name='reading-materials-delete'),
    
    # Users
    path("users/",views.UserListView.as_view(),name="user-list",),
    path("users/add/",views.UserCreateView.as_view(),name="user-add",),
    path("users/edit/<int:pk>/",views.UserUpdateView.as_view(),name="user-edit",),
    path("users/delete/<int:pk>/",views.UserDeleteView.as_view(),name="user-delete",),
    
    
    path("ratings/",views.RatingsListCreateView.as_view(),name="ratings-list-create",),
]