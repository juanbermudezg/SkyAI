from django.urls import path
from .views import PostDetailView, PostListView

app_name='sky'

urlpatterns = [
    path('', PostListView.as_view(), name="main"),
    path('<pk>/', PostDetailView.as_view(), name="detail")
]