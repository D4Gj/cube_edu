from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from .fields import OrderField, NonStrippingTextField
from ckeditor.fields import RichTextField
from problem.models import Problem
from multiselectfield import MultiSelectField


class Subject(models.Model):
    title = models.CharField(verbose_name="Название предмета", max_length=200)
    slug = models.SlugField(verbose_name="Slug в строке", max_length=200, unique=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Название курса", max_length=200)
    slug = models.SlugField(verbose_name="Slug в строке", max_length=200, unique=True)
    overview = models.TextField(verbose_name="Краткое описание")
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)

    class Meta:
        ordering = ['-created']
        verbose_name = "Курсы"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Название", max_length=200)
    description = models.TextField(verbose_name="Краткое описание", blank=True)
    order = OrderField(blank=True, for_fields=['course'])
    visible = models.BooleanField("Видимость обучающимся", blank=False, null=False, default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE,
                               limit_choices_to={'model__in': (
                                   'text',
                                   'video',
                                   'image',
                                   'file',
                                   'code'
                               )})
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Название", max_length=250, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    visible = models.BooleanField("Видимость контента", blank=False, null=False, default=False)
    problem_solve = models.OneToOneField(Problem, on_delete=models.SET_NULL, null=True, blank=True, )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.title if self.title else 'Без названия'}|{'Открыт всем' if self.visible else 'Закрыт'} {self.problem_solve.title if self.problem_solve else 'Без задачи'} "

    def render(self):
        return render_to_string(f'courses/content/{self._meta.model_name}.html',
                                {'item': self})


class Text(ItemBase):
    content = RichTextField(verbose_name="Контент")


class File(ItemBase):
    file = models.FileField(upload_to='files', verbose_name="Файл")


class Image(ItemBase):
    file = models.FileField(verbose_name="Файл", upload_to='images')


class Video(ItemBase):
    url = models.URLField()


class Code(ItemBase):
    code = NonStrippingTextField()
    input_data = NonStrippingTextField(blank=True, null=True)

    def __str__(self):
        return self.title if self.title else "code without name"
