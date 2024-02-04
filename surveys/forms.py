from django import forms

from surveys.models import Answer


class TextModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.text


class AnswerForm(forms.Form):
    answer = TextModelChoiceField(
        queryset=Answer.objects.all(),
        widget=forms.RadioSelect,
        label='Выберите ответ',
    )

    def __init__(self, *args, **kwargs):
        answers = kwargs.pop('answers', None)
        super(AnswerForm, self).__init__(*args, **kwargs)
        if answers:
            self.fields['answer'].queryset = answers
