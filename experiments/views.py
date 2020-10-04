from django.shortcuts import render
from .filters import ExperimentFilter
from .models import Experiment


def experiments_list(request):
    experiment_list = Experiment.objects.all()
    tableFilter = ExperimentFilter(request.GET, queryset=experiment_list)
    context = {'experiments': experiment_list, 'tableFilter': tableFilter}
    return render(request, 'experiments/experiments_list.html', context)
