from django import forms
from .models import SchemaTemplate, SchemaTemplateColumn


class SchemaForm(forms.ModelForm):
    class Meta:
        model = SchemaTemplate
        fields = ('title', 'column_separator', 'string_character')


class SchemaColumnForm(forms.ModelForm):
    class Meta:
        model = SchemaTemplateColumn
        exclude = ['schema']


SchemaColumnFormset = forms.inlineformset_factory(SchemaTemplate, SchemaTemplateColumn,
                          form=SchemaColumnForm, can_delete=True, extra=1)
