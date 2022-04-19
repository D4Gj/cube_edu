from django.contrib.auth.models import User
from django.db import models
from django.forms import JSONField
from courses.fields import NonStrippingTextField


class Problem(models.Model):
    # for contest problem
    title = models.TextField(verbose_name="Название")
    # HTML
    description = models.TextField(verbose_name="Описание задачи")
    input_description = models.TextField(verbose_name="Входные данные")
    output_description = models.TextField(verbose_name="Выходные данные")
    problem_tests_input = JSONField()
    problem_tests_output = JSONField()
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    # we can not use auto_now here
    last_update_time = models.DateTimeField(auto_now_add=True, verbose_name="Обновлено")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # ms
    time_limit = models.IntegerField(verbose_name="Ограничение по времени")
    # MB
    memory_limit = models.IntegerField(verbose_name="Ограничение по памяти")
    visible = models.BooleanField(verbose_name="Открыта для всех", default=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    user = models.ForeignKey(User, verbose_name="Автор", related_name="submissions", on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, verbose_name="Задача", related_name="submissions", on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="Время попытки", auto_now_add=True)
    code = NonStrippingTextField()
    # 0 - Accepted; 1-Wrong answer; 2-Compilation error;3 - Time error; 4 - Memory error
    result = models.IntegerField()

    class Meta:
        ordering = ('-date',)

    def date_string(self):
        return self.date.strftime('%d-%m-%Y %H:%M:%S')
