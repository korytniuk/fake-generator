from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import SchemaTemplate, SchemaTemplateColumn, DataSet
from .forms import SchemaForm, SchemaColumnFormset


def index(request):
    return render(request, "generator/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "generator/login.html", {
                "message": "Invalid Username or Password."
            })
    else:
        return render(request, "generator/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


class DataSetList(LoginRequiredMixin, generic.ListView):
    context_object_name = 'datasets'
    template_name = 'generator/dataset_list.html'

    def get_queryset(self):
        return DataSet.objects.\
            filter(schema=self.kwargs['id']).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        # todo call generator function
        schema_id = kwargs.get('id')
        print(request.POST)
        return HttpResponseRedirect(reverse('datasets', args=[schema_id]))


class SchemaTemplateList(LoginRequiredMixin, generic.ListView):
    context_object_name = 'schemas'
    queryset = SchemaTemplate.objects.filter(
        deleted=False).order_by('-updated_at')
    template_name = 'generator/schema_list.html'


@login_required
@require_http_methods(["GET", "POST"])
def schema_edit(request, id):
    instance = get_object_or_404(SchemaTemplate, id=id)
    form = SchemaForm(request.POST or None, instance=instance)
    formset = SchemaColumnFormset(request.POST or None, instance=instance)

    if request.method == "POST" and form.is_valid() and formset.is_valid():
        instance = form.save()
        formset.save()

        return HttpResponseRedirect(
            reverse('datasets', args=[instance.id]))

    print('test', formset.errors)

    return render(request, "generator/schema_edit.html",
                  {'form': form, 'formset': formset})


@login_required
@require_http_methods(["GET", "POST"])
def schema_create(request):
    form = SchemaForm()
    formset = SchemaColumnFormset(instance=SchemaTemplate())

    if request.method == "POST":
        form = SchemaForm(request.POST)
        if form.is_valid():
            instance = form.save()
            formset = SchemaColumnFormset(request.POST, instance=instance)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect(
                    reverse('datasets', args=[instance.id]))

    return render(request, "generator/schema_create.html",
                  {'form': form, 'formset': formset})


@require_http_methods(["DELETE"])
@login_required
def schema_delete(request, id):
    item = get_object_or_404(SchemaTemplate, pk=id)
    item.deleted = True
    item.save()

    return HttpResponse("Success", status=200)


@require_POST
def generate_fake_data(request, id):
    pass
