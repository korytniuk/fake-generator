from django.contrib import admin
from .models import DataSet, SchemaTemplate,\
    SchemaTemplateColumn, SchemaColumnType

# Register your models here.
admin.site.register(DataSet)
admin.site.register(SchemaTemplate)
admin.site.register(SchemaTemplateColumn)
admin.site.register(SchemaColumnType)
