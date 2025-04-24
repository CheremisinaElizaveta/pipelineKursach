from django.urls import include, path
from tests.views_psych_admin import *
import debug_toolbar

app_name = "psych_admin"

urlpatterns = [
    path('', admin, name="index"),
    path('__debug__/', include(debug_toolbar.urls)),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name="category_create"),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', delete_category, name='category_delete'),
    
    path('tendencies/', TendencyListView.as_view(), name='tendency_list'),
    path('tendencies/create/', TendencyCreateView.as_view(), name="tendency_create"),
    path('tendencies/<int:pk>/update/', TendencyUpdateView.as_view(), name='tendency_update'),
    path('tendencies/<int:pk>/delete/', delete_tendency, name='tendency_delete'),
    
    path('types_question/', QuestionTypeListView.as_view(), name='question_type_list'),
    path('types_question/create/', QuestionTypeCreateView.as_view(), name="question_type_create"),
    path('types_question/<int:pk>/update/', QuestionTypeUpdateView.as_view(), name='question_type_update'),
    path('types_question/<int:pk>/delete/', delete_question_type, name='question_type_delete'),
    
    path('activities/', ActivityListView.as_view(), name='activity_list'),
    path('activities/create/', ActivityCreateView.as_view(), name="activity_create"),
    path('activities/<int:pk>/update/', ActivityUpdateView.as_view(), name='activity_update'),
    path('activities/<int:pk>/delete/', delete_activity, name='activity_delete'),
    
    path('personalities/', PersonalityListView.as_view(), name='personality_list'),
    path('personalities/create/', PersonalityCreateView.as_view(), name="personality_create"),
    path('personalities/<int:pk>/update/', PersonalityUpdateView.as_view(), name='personality_update'),
    path('personalities/<int:pk>/delete/', delete_personality, name='personality_delete'),
    
    path('tests/', TestListView.as_view(), name='test_list'),
    path('tests/create/', TestCreateView.as_view(), name="test_create"),
    path('tests/<int:pk>/', TestDetailView.as_view(), name="test_detail"),
    path('tests/<int:pk>/update/', TestUpdateView.as_view(), name='test_update'),
    path('tests/<int:pk>/delete/', delete_test, name='test_delete'),
]
