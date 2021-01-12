from django.urls import path
from .views import *

urlpatterns = [
    path('', post_list, name='index'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/', post_detail, name='post-detail'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path("review/<int:pk>/", AddReview.as_view(), name="add_review"),
]

