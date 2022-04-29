import asyncio

from asgiref.sync import sync_to_async, async_to_sync
from django.core.exceptions import ValidationError
from django.forms import forms
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView
from .models import Problem, Submission
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .utils import check_submission
import json


class CreateProblemView(PermissionRequiredMixin, CreateView):
    model = Problem
    template_name = "problems/manage/create.html"
    fields = ['title',
              'description',
              'description_input',
              'description_output',
              'time_limit',
              'memory_limit',
              'visible']
    permission_required = 'problems.add_problem'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if request is not None and form.is_valid():
            data = request.POST
            inputs = dict()
            outputs = dict()
            for key, val in data.items():
                if key[:2] == 'in':
                    inputs[key] = val.replace("\r", "") + "\n"
                elif key[:3] == 'out':
                    outputs[key] = val.replace("\r", "") + "\n"
            if inputs['in1'] or outputs['out1']:
                problem = Problem(title=data['title'],
                                  description=data['description'],
                                  description_input=data['description_input'],
                                  description_output=data['description_output'],
                                  created_by=request.user,
                                  time_limit=int(data['time_limit']),
                                  memory_limit=int(data['memory_limit']),
                                  visible=True if data['visible'] == 'on' else False,
                                  problem_tests_input=json.dumps(inputs),
                                  problem_tests_output=json.dumps(outputs))
                problem.save()
                return redirect('detail_problem', pk=problem.id)
            else:
                return render(request, 'problems/manage/create.html', {'form': form})
        else:
            return render(request, 'problems/manage/create.html', {'form': form})


class DetailProblemView(DetailView):
    model = Problem
    template_name = "problems/problem/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = get_object_or_404(Problem, pk=self.kwargs['pk'])
        data_dict_input = json.loads(data.problem_tests_input)
        data_dict_output = json.loads(data.problem_tests_output)
        samples = dict()
        for i in range(1, len(data_dict_input) + 1):
            samples[f'test{i}'] = [
                data_dict_input[f'in{i}'],
                data_dict_output[f'out{i}']
            ]
            if i == 3:
                break
        context['samples'] = samples
        if self.request.user.is_authenticated:
            context['submissions'] = Submission.objects.filter(
                user=self.request.user,
                problem=get_object_or_404(
                    Problem,
                    pk=self.kwargs['pk']
                )
            )
        return context

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        if code:
            problem = self.get_object()
            submission = Submission(
                user=request.user,
                problem=problem,
                code=code,
                description="Проверяется",
                result=-1
            )
            submission.save()
            check_submission(code, submission, problem)
            return HttpResponse('checking')
        else:
            return HttpResponse('error')


class ListProblemView(ListView):
    model = Problem
    template_name = "problems/problem/list.html"
    context_object_name = "problems"

    def get_context_data(self, **kwargs):
        context = super(ListProblemView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['result'] = Submission.objects.filter(user=self.request.user)
        return context
