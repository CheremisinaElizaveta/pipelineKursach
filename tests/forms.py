from django import forms
from tests.models import (
    Test,
    Result,
    Question,
    Variant,
    AssigningTest,
    TestResult,
    Status,
    Category,
    QuestionType,
    Personality
)
from django.utils import timezone
from users.models import Tendency, Activity, PersonalityRecommendation


class SetQuestionsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.questions = kwargs.pop('questions')
        self.test = kwargs.pop('test')
        self.user = kwargs.pop('user')
        self.assign_test = kwargs.pop('assign_test')
        super().__init__(*args, **kwargs)

        for question in self.questions:
            variants = question.variant_set.all()
            choices = [(variant.id, variant.text) for variant in variants]

            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text,
                choices=choices,
                widget=forms.RadioSelect,
                required=True,
            )
            
    def clean(self):
        cleaned_data = super().clean()
        
        if self.assign_test.due_datetime <= timezone.now():
            previous_test_result_exists = TestResult.objects.filter(
                user=self.user,
                test=self.test
            ).exists()

            if previous_test_result_exists:
                raise forms.ValidationError("Срок теста подошел к концу. Вы уже проходили этот тест.")
            else:
                status, _ = Status.objects.get_or_create(name='не завершен')
                self.assign_test.status = status
                self.assign_test.save()

                raise forms.ValidationError("Срок теста подошел к концу. Вы не успели пройти тест.")

        total_scores = 0

        for question in self.questions:
            field_name = f'question_{question.id}'
            variant_id = cleaned_data.get(field_name)
            if variant_id:
                try:
                    variant = Variant.objects.get(id=variant_id)
                    total_scores += variant.scores
                except Variant.DoesNotExist:
                    raise forms.ValidationError(f"Вариант с ID {variant_id} не найден.")

        result = Result.objects.filter(
            test=self.test,
            min_score__lte=total_scores,
            max_score__gte=total_scores
        ).first()

        if result:
            self.cleaned_data['result'] = result
            self.cleaned_data['total_scores'] = total_scores
            return self.cleaned_data

        raise forms.ValidationError("Не удалось определить результат для полученного количества баллов.")
        
    
    def save(self):
        result = self.cleaned_data['result']
        
        previous_test_result = TestResult.objects.filter(
            user=self.user,
            test=self.test,
        )
        if previous_test_result:
            previous_test_result.delete()

        TestResult.objects.create(
            scores=self.cleaned_data['total_scores'],
            result=result,
            user=self.user,
            test=self.test
        )

        if self.test.trial and not self.user.personality_type:
            self.user.personality_type = result.personality_type
        
        self.user.types_activities.add(*result.types_activities.all())
        self.user.tendencies.add(*result.tendencies.all())
        if result.personality_recommendations:
            self.user.personality_recommendations.add(result.personality_recommendations)

        self.user.save()
        
        status, _ = Status.objects.get_or_create(name='завершен')
        AssigningTest.objects.filter(user=self.user, test=self.test).update(status=status)


class CreateTestForm(forms.ModelForm):    
    class Meta:
        model = Test
        fields = (
            "preview",
            "illustration",
            "name",
            "category",
            "description",
            "trial"
        )
    
    def clean(self):
        cleaned_data = super().clean()
        trial = cleaned_data.get("trial")

        if trial:
            qs = Test.objects.filter(trial=True)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Можно создать только один пробный тест.")

        return cleaned_data


class CreateResultForm(forms.ModelForm):
    types_activities = forms.ModelMultipleChoiceField(
        queryset=Activity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Рекомендованные виды деятельности"
    )
    tendencies = forms.ModelMultipleChoiceField(
        queryset=Tendency.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Склонности для результата",
    )
    personality_recommendations_text = forms.CharField(
        label="Персональные рекомендации",
        widget=forms.Textarea,
        required=False
    )
    
    class Meta:
        model = Result
        fields = (
            "text",
            "min_score",
            "max_score",
            "types_activities",
            "personality_type",
            "tendencies",
        )
        
    def save(self, commit=True):
        recommendations_text = self.cleaned_data.get("personality_recommendations_text")
        recommendation = PersonalityRecommendation.objects.create(text=recommendations_text)

        result = super().save(commit=False)
        result.personality_recommendations = recommendation

        if commit:
            result.save()
            self.save_m2m()

        return result
        

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['type', 'text', 'order']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['order'].label = 'Номер вопроса'

        if self.instance and self.instance.pk:
            self.fields['order'].required = True
        else:
            self.fields['order'].required = False

VariantFormSet = forms.inlineformset_factory(
    Question, Variant,
    fields=('text', 'scores'),
    extra=1, can_delete=True
)


class SetTestForm(forms.ModelForm):
    class Meta:
        model = AssigningTest
        fields = (
            "due_datetime",
            "user",
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class TendencyForm(forms.ModelForm):
    class Meta:
        model = Tendency
        fields = ('name',)
        
class QuestionTypeForm(forms.ModelForm):
    class Meta:
        model = QuestionType
        fields = ('name',)
        

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('name', 'description')
        

class PersonalityForm(forms.ModelForm):
    class Meta:
        model = Personality
        fields = ('name', 'recommendations')
