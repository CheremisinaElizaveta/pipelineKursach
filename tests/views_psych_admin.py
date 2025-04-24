import logging
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from tests.decorators import psych_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from tests.models import Category, QuestionType, Test
from users.models import Tendency, Activity, Personality
from tests.forms import (
    CategoryForm, 
    TendencyForm, 
    QuestionTypeForm, 
    ActivityForm,
    PersonalityForm,
    CreateTestForm
)


@psych_required()
def admin(request):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Логируем открытие страницы
    logging.info(f"Пользователь '{request.user.username}' открыл страницу администратора")
    return render(request, "tests/psych_admin/admin_index.html")

# categories
@method_decorator(psych_required(), name="dispatch")
class CategoryListView(ListView):
    model = Category
    template_name = 'tests/psych_admin/categories/category_list.html'
    context_object_name = 'categories'

    def get(self, request, *args, **kwargs):
        # Логируем открытие страницы
        logging.info(f"Пользователь '{request.user.username}' открыл список категорий")
        return super().get(request, *args, **kwargs)

@method_decorator(psych_required(), name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tests/psych_admin/categories/category_form.html'
    success_url = reverse_lazy('psych_admin:category_list')

    def form_valid(self, form):
        # Логируем создание категории
        logging.info(f"Пользователь '{self.request.user.username}' создал новую категорию '{form.instance.name}'")
        return super().form_valid(form)

@method_decorator(psych_required(), name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tests/psych_admin/categories/category_form.html'
    success_url = reverse_lazy('psych_admin:category_list')

    def form_valid(self, form):
        # Логируем обновление категории
        logging.info(f"Пользователь '{self.request.user.username}' обновил категорию '{form.instance.name}'")
        return super().form_valid(form)

@psych_required()
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    # Логируем удаление категории
    logging.info(f"Пользователь '{request.user.username}' удалил категорию '{category.name}'")
    category.delete()
    return redirect('psych_admin:category_list')

# tendencies
@method_decorator(psych_required(), name="dispatch")
class TendencyListView(ListView):
    model = Tendency
    template_name = 'tests/psych_admin/tendencies/tendency_list.html'
    context_object_name = 'tendencies'

    def get(self, request, *args, **kwargs):
        # Логируем открытие страницы
        logging.info(f"Пользователь '{request.user.username}' открыл список тенденций")
        return super().get(request, *args, **kwargs)

@method_decorator(psych_required(), name="dispatch")
class TendencyCreateView(CreateView):
    model = Tendency
    form_class = TendencyForm
    template_name = 'tests/psych_admin/tendencies/tendency_form.html'
    success_url = reverse_lazy('psych_admin:tendency_list')

    def form_valid(self, form):
        # Логируем создание тенденции
        logging.info(f"Пользователь '{self.request.user.username}' создал новую тенденцию '{form.instance.name}'")
        return super().form_valid(form)

@method_decorator(psych_required(), name="dispatch")
class TendencyUpdateView(UpdateView):
    model = Tendency
    form_class = TendencyForm
    template_name = 'tests/psych_admin/tendencies/tendency_form.html'
    success_url = reverse_lazy('psych_admin:tendency_list')

    def form_valid(self, form):
        # Логируем обновление тенденции
        logging.info(f"Пользователь '{self.request.user.username}' обновил тенденцию '{form.instance.name}'")
        return super().form_valid(form)

@psych_required()
def delete_tendency(request, pk):
    tendency = get_object_or_404(Tendency, pk=pk)
    # Логируем удаление тенденции
    logging.info(f"Пользователь '{request.user.username}' удалил тенденцию '{tendency.name}'")
    tendency.delete()
    return redirect('psych_admin:tendency_list')

# types_question
@method_decorator(psych_required(), name="dispatch")
class QuestionTypeListView(ListView):
    model = QuestionType
    template_name = 'tests/psych_admin/types_question/question_type_list.html'
    context_object_name = 'types_question'

    def get(self, request, *args, **kwargs):
        # Логируем открытие страницы
        logging.info(f"Пользователь '{request.user.username}' открыл список типов вопросов")
        return super().get(request, *args, **kwargs)

@method_decorator(psych_required(), name="dispatch")
class QuestionTypeCreateView(CreateView):
    model = QuestionType
    form_class = QuestionTypeForm
    template_name = 'tests/psych_admin/types_question/question_type_form.html'
    success_url = reverse_lazy('psych_admin:question_type_list')

    def form_valid(self, form):
        # Логируем создание типа вопроса
        logging.info(f"Пользователь '{self.request.user.username}' создал новый тип вопроса '{form.instance.name}'")
        return super().form_valid(form)

@method_decorator(psych_required(), name="dispatch")
class QuestionTypeUpdateView(UpdateView):
    model = QuestionType
    form_class = QuestionTypeForm
    template_name = 'tests/psych_admin/types_question/question_type_form.html'
    success_url = reverse_lazy('psych_admin:question_type_list')

    def form_valid(self, form):
        # Логируем обновление типа вопроса
        logging.info(f"Пользователь '{self.request.user.username}' обновил тип вопроса '{form.instance.name}'")
        return super().form_valid(form)

@psych_required()
def delete_question_type(request, pk):
    question_type = get_object_or_404(QuestionType, pk=pk)
    # Логируем удаление типа вопроса
    logging.info(f"Пользователь '{request.user.username}' удалил тип вопроса '{question_type.name}'")
    question_type.delete()
    return redirect('psych_admin:question_type_list')

# activities
@method_decorator(psych_required(), name="dispatch")
class ActivityListView(ListView):
    model = Activity
    template_name = 'tests/psych_admin/activities/activity_list.html'
    context_object_name = 'activities'

    def get(self, request, *args, **kwargs):
        # Логируем открытие страницы
        logging.info(f"Пользователь '{request.user.username}' открыл список активностей")
        return super().get(request, *args, **kwargs)

@method_decorator(psych_required(), name="dispatch")
class ActivityCreateView(CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'tests/psych_admin/activities/activity_form.html'
    success_url = reverse_lazy('psych_admin:activity_list')

    def form_valid(self, form):
        # Логируем создание активности
        logging.info(f"Пользователь '{self.request.user.username}' создал новую активность '{form.instance.name}'")
        return super().form_valid(form)

@method_decorator(psych_required(), name="dispatch")
class ActivityUpdateView(UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'tests/psych_admin/activities/activity_form.html'
    success_url = reverse_lazy('psych_admin:activity_list')

    def form_valid(self, form):
        # Логируем обновление активности
        logging.info(f"Пользователь '{self.request.user.username}' обновил активность '{form.instance.name}'")
        return super().form_valid(form)

@psych_required()
def delete_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    # Логируем удаление активности
    logging.info(f"Пользователь '{request.user.username}' удалил активность '{activity.name}'")
    activity.delete()
    return redirect('psych_admin:activity_list')

# personalities
@method_decorator(psych_required(), name="dispatch")
class PersonalityListView(ListView):
    model = Personality
    template_name = 'tests/psych_admin/personalities/personality_list.html'
    context_object_name = 'personalities'

    def get(self, request, *args, **kwargs):
        # Логируем открытие страницы
        logging.info(f"Пользователь '{request.user.username}' открыл список личностей")
        return super().get(request, *args, **kwargs)

@method_decorator(psych_required(), name="dispatch")
class PersonalityCreateView(CreateView):
    model = Personality
    form_class = PersonalityForm
    template_name = 'tests/psych_admin/personalities/personality_form.html'
    success_url = reverse_lazy('psych_admin:personality_list')

    def form_valid(self, form):
        # Логируем создание личности
        logging.info(f"Пользователь '{self.request.user.username}' создал новую личность '{form.instance.name}'")
        return super().form_valid(form)

@method_decorator(psych_required(), name="dispatch")
class PersonalityUpdateView(UpdateView):
    model = Personality
    form_class = PersonalityForm
    template_name = 'tests/psych_admin/personalities/personality_form.html'
    success_url = reverse_lazy('psych_admin:personality_list')

    def form_valid(self, form):
        # Логируем обновление личности
        logging.info(f"Пользователь '{self.request.user.username}' обновил личность '{form.instance.name}'")
        return super().form_valid(form)

@psych_required()
def delete_personality(request, pk):
    personality = get_object_or_404(Personality, pk=pk)
    # Логируем удаление личности
    logging.info(f"Пользователь '{request.user.username}' удалил личность '{personality.name}'")
    personality.delete()
    return redirect('psych_admin:personality_list')

@method_decorator(psych_required(), name="dispatch")
class TestListView(ListView):
    model = Test
    template_name = 'tests/psych_admin/tests/test_list.html'
    context_object_name = 'tests'
    
    def get(self, request, *args, **kwargs):
        # Логируем открытие страницы
        logging.info(f"Пользователь '{request.user.username}' открыл список тестов")
        return super().get(request, *args, **kwargs)

@method_decorator(psych_required(), name="dispatch")
class TestDetailView(DetailView):
    model = Test
    template_name = 'tests/psych_admin/tests/test_detail.html'
    context_object_name = 'test'

    def get(self, request, *args, **kwargs):
        # Логируем открытие страницы
        logging.info(f"Пользователь '{request.user.username}' открыл детали теста")
        return super().get(request, *args, **kwargs)

@method_decorator(psych_required(), name="dispatch")
class TestCreateView(CreateView):
    model = Test
    form_class = CreateTestForm
    template_name = 'tests/psych_admin/tests/test_form.html'
    success_url = reverse_lazy('psych_admin:test_list')

    def form_valid(self, form):
        # Логируем создание теста
        logging.info(f"Пользователь '{self.request.user.username}' создал новый тест '{form.instance.name}'")
        return super().form_valid(form)

@method_decorator(psych_required(), name="dispatch")
class TestUpdateView(UpdateView):
    model = Test
    form_class = CreateTestForm
    template_name = 'tests/psych_admin/tests/test_form.html'
    success_url = reverse_lazy('psych_admin:test_list')

    def form_valid(self, form):
        # Логируем обновление теста
        logging.info(f"Пользователь '{self.request.user.username}' обновил тест '{form.instance.name}'")
        return super().form_valid(form)

@psych_required()
def delete_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    # Логируем удаление теста
    logging.info(f"Пользователь '{request.user.username}' удалил тест '{test.name}'")
    test.delete()
    return redirect('psych_admin:test_list')
