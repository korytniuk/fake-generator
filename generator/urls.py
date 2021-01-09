from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("schemas/", views.SchemaTemplateList.as_view(), name="schema_list"),
    path("schema_delete/<int:id>/", views.schema_delete, name="schema_delete"),
    path("schema_edit/<int:id>/", views.schema_edit, name="schema_edit"),
    path("schema_create/", views.schema_create, name="schema_create"),
    path("datasets/<int:id>/", views.DataSetList.as_view(), name="datasets"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
