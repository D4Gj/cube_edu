from django.urls import path
from .views import DetailProblemView, ListProblemView, CreateProblemView

urlpatterns = [
    path('detail/<pk>/', DetailProblemView.as_view(), name="detail_problem"),
    path('list/', ListProblemView.as_view(), name="list_problems"),
    path('create/', CreateProblemView.as_view(), name="create_problem"),
]
