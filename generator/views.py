from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from celery import current_app

from .models import SchemaTemplate, DataSet
from .forms import SchemaForm, SchemaColumnFormset
from .tasks import generate_fake_file
from .util import READY_STATUS


@login_required
def index(request):
    return HttpResponseRedirect(reverse('schema_list'))


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


@login_required
@require_http_methods(["GET", "POST"])
def dataset_list(request, id):
    schema_id = int(id)
    task_id = None
    task_status = None

    if request.method == 'POST':
        rows = int(request.POST.get('rows'))
        schema = get_object_or_404(SchemaTemplate, id=schema_id)
        dataset = DataSet(schema=schema)
        dataset.save()
        task = generate_fake_file.delay(dataset.id, rows)
        task_id = task.id
        task_status = task.status

    datasets = DataSet.objects.filter(schema=schema_id).order_by('-created_at')

    return render(request, "generator/dataset_list.html",
                  context={'datasets': datasets,
                           'READY_STATUS': READY_STATUS,
                           "task_id": task_id,
                           "task_status": task_status})


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


class TaskView(generic.View):
    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}

        return JsonResponse(response_data)
