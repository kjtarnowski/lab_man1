from django.shortcuts import render
from .filters import ExperimentFilter, ResultFilter
from .models import Experiment, Result
from .forms import ExperimentForm, ResultForm


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


def results_list(request):
    results_list = Result.objects.all()
    tableFilter = ResultFilter(request.GET, queryset=results_list)
    context = {'results': results_list, 'tableFilter': tableFilter}
    return render(request, 'experiments/results_list.html', context)


def edit_result(request, result_id):
    result_instance = Result.objects.get(id=result_id)
    if request.method == 'POST':
        result_form = ResultForm(data=request.POST, instance=result_instance)
        if result_form.is_valid():
            result_form.save()
    else:
        result_form = ResultForm(instance=result_instance)
    return render(
        request,
        'experiments/edit_result.html',
        {'result_form': result_form}
    )
