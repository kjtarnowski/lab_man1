from django.shortcuts import render, get_object_or_404
from .filters import ExperimentFilter
from .models import Experiment
from .forms import ExperimentForm


def experiments_list(request):
    experiment_list = Experiment.objects.all()
    tableFilter = ExperimentFilter(request.GET, queryset=experiment_list)
    context = {'experiments': experiment_list, 'tableFilter': tableFilter}
    return render(request, 'experiments/experiments_list.html', context)


def edit_experiment(request, experiment_id):
    experiment_instance = Experiment.objects.get(id=experiment_id)
    if request.method == 'POST':
        experiment_form = ExperimentForm(data=request.POST, instance=experiment_instance)
        if experiment_form.is_valid():
            experiment_form.save()
    else:
        experiment_form = ExperimentForm(instance=experiment_instance)
    return render(
        request,
        'experiments/edit_experiment.html',
        {'experiment_form': experiment_form}
    )
