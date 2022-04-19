from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from .models import Problem
from django.shortcuts import redirect


class CreateProblemView(CreateView):
    model = Problem
    template_name = "problems/manage/create.html"
    fields = '__all__'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        if request is not None:
            Problem.objects.create(title=request.POST['title'], description=request.POST['description'],
                                   input_description=request.POST['input_description'],
                                   output_description=request.POST['output_description'],
                                   visible=False,
                                   created_by=request.user,
                                   time_limit=request.POST['time_limit'],
                                   memory_limit=request.POST['memory_limit'],
                                   )
        return redirect('mine')


class DetailProblemView(DetailView):
    model = Problem
    template_name = "problems/problem/detail.html"
    fields = '__all__'


class ListProblemView(ListView):
    model = Problem
    template_name = "problems/problem/list.html"
    context_object_name = "problems"
