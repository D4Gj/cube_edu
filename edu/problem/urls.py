from django.urls import path
from .views import DetailProblemView, ListProblemView, CreateProblemView, UpdateProblemView, ProblemDeleteView

urlpatterns = [
    path('detail/<pk>/', DetailProblemView.as_view(), name="detail_problem"),
    path('list/', ListProblemView.as_view(), name="list_problems"),
    path('create/', CreateProblemView.as_view(), name="create_problem"),
    path('update/<pk>/', UpdateProblemView.as_view(), name='update_problem'),
    path('delete/<pk>/', ProblemDeleteView.as_view(), name='delete_problem')
]
