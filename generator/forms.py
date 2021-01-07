from django import forms
from .models import SchemaTemplate, SchemaTemplateColumn, SchemaColumnType
from .util import SEPARATOR_CHOICES


class SchemaForm(forms.ModelForm):
    column_separator = forms.ChoiceField(choices=SEPARATOR_CHOICES)

    class Meta:
        model = SchemaTemplate
        fields = ('title', 'column_separator')


class SchemaColumnForm(forms.ModelForm):
    class Meta:
        model = SchemaTemplateColumn
        exclude = ['schema']


SchemaColumnFormset = forms.inlineformset_factory(SchemaTemplate, SchemaTemplateColumn,
                          form=SchemaColumnForm, can_delete=True, extra=1)
