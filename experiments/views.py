import csv, io
from django.shortcuts import render
from .filters import ExperimentFilter, ResultFilter, CompoundFilter
from .models import Experiment, Result, Compound, Project
from .forms import ExperimentForm, ResultForm, CompoundForm
from django.contrib import messages


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


def compound_list(request):
    compound_list = Compound.objects.all()
    tableFilter = CompoundFilter(request.GET, queryset=compound_list)
    context = {'experiments': compound_list, 'tableFilter': tableFilter}
    return render(request, 'experiments/compounds_list.html', context)


def edit_compound(request, compound_id):
    compound_instance = Compound.objects.get(id=compound_id)
    if request.method == 'POST':
        compound_form = CompoundForm(data=request.POST, instance=compound_instance)
        if compound_form.is_valid():
            compound_form.save()
    else:
        compound_form = CompoundForm(instance=compound_instance)
    return render(
        request,
        'experiments/edit_compound.html',
        {'compound_form': compound_form}
    )


def compounds_upload(request):
    if request.method == "GET":
        return render(request, "experiments/upload_compounds.html", {})
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Compound.objects.update_or_create(
            compound_name=column[0],
            compound_mass=column[1],
            compound_monoisotopic_mass=column[2],
            compound_formula=column[3],
            comments=column[4],
            project=Project.objects.filter(project_name=column[5])[0]
        )
    return render(
        request,
        "experiments/upload_compounds.html",
        {}
    )
