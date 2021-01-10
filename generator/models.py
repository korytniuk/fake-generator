from django.db import models
from django.contrib.auth.models import User
from .util import STATUS_CHOICES, PENDING_STATUS, SEPARATOR_CHOICES, COMMA, DOUBLE_QUOTE, QUOTE_CHOICES


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract: True


class SchemaTemplate(TimeStampMixin):
    title = models.CharField(max_length=255)
    column_separator = models.SmallIntegerField(
        choices=SEPARATOR_CHOICES, default=COMMA)
    string_character = models.SmallIntegerField(
        choices=QUOTE_CHOICES, default=DOUBLE_QUOTE)

    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class SchemaColumnType(TimeStampMixin):
    name = models.CharField(max_length=255)
    has_range = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SchemaTemplateColumn(models.Model):
    schema = models.ForeignKey(
        SchemaTemplate, on_delete=models.CASCADE, related_name="columns")
    name = models.CharField(max_length=255)
    order = models.SmallIntegerField()
    range_from = models.IntegerField(default=None, null=True, blank=True)
    range_to = models.IntegerField(default=None, null=True, blank=True)
    column_type = models.ForeignKey(
        SchemaColumnType, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class DataSet(TimeStampMixin):
    schema = models.ForeignKey(SchemaTemplate, on_delete=models.DO_NOTHING)
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES, default=PENDING_STATUS)
    link = models.FileField(default=None, null=True,
                            blank=True)

    def __str__(self):
        return str(self.schema) + ' ' + self.get_status_display()
