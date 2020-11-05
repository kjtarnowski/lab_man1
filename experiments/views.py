import csv
from datetime import datetime
import io

from django.contrib import messages
from django.shortcuts import render

from .filters import ExperimentFilter, CompoundFilter
from .forms import ExperimentForm, CompoundForm
from .models import Experiment, Compound, Project, ExperimentalSet, \
 Aparat, LabPerson


def experiments_list(request):
    experiment_list = Experiment.objects.all()
    tableFilter = ExperimentFilter(request.GET, queryset=experiment_list)
    context = {'experiments': experiment_list, 'tableFilter': tableFilter}
    return render(request, 'experiments/experiments_list.html', context)


def edit_experiment(request, experiment_id):
    experiment_instance = Experiment.objects.get(id=experiment_id)
    if request.method == 'POST':
        experiment_form = ExperimentForm(
            data=request.POST,
            instance=experiment_instance
            )
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
    experiment_list = Experiment.objects.all()
    tableFilter = ExperimentFilter(request.GET, queryset=experiment_list)
    context = {'experiments': experiment_list, 'tableFilter': tableFilter}
    return render(request, 'experiments/results_list.html', context)


def compound_list(request):
    compound_list = Compound.objects.all()
    tableFilter = CompoundFilter(request.GET, queryset=compound_list)
    context = {'experiments': compound_list, 'tableFilter': tableFilter}
    return render(request, 'experiments/compounds_list.html', context)


def edit_compound(request, compound_id):
    compound_instance = Compound.objects.get(id=compound_id)
    if request.method == 'POST':
        compound_form = CompoundForm(
            data=request.POST,
            instance=compound_instance)
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
        try:
            obj = Compound.objects.get(name=column[0])
            obj.mass = column[1]
            obj.monoisotopic_mass = column[2]
            obj.formula = column[3]
            obj.comments = column[4]
            obj.comments = column[5]
            obj.save()
        except Compound.DoesNotExist:
            Compound.objects.create(
                name=column[0],
                mass=column[1],
                monoisotopic_mass=column[2],
                formula=column[3],
                comments=column[4],
                project=Project.objects.filter(name=column[5])[0]
            )
    return render(
        request,
        "experiments/upload_compounds.html",
        {}
    )


def experiments_upload(request):
    if request.method == "GET":
        return render(request, "experiments/upload_experiments.html", {})
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    # next(io_string)
    for n, column in enumerate(csv.reader(io_string, delimiter=',', quotechar="|")):
        if n == 0:
            results_names = []
            for i in range(9, len(column)):
                if column[i]:
                    results_names.append(column[i])
        else:
            try:
                exp_set_obj = ExperimentalSet.objects.get(name=column[3])
            except ExperimentalSet.DoesNotExist:
                exp_set_obj = ExperimentalSet.objects.create(
                    name=column[3],
                    experiment_date=datetime.strptime(column[2], '%Y-%m-%d').date()
                )
            try:
                obj = Experiment.objects.get(
                    compound=Compound.objects.get(name=column[0]),
                    experimental_set=exp_set_obj
                    )
                obj.experiment_date = datetime.strptime(column[2], '%Y-%m-%d').date()
                obj.aparat = Aparat.objects.filter(name=column[4]).get()
                obj.lab_person = LabPerson.objects.filter(name=column[5]).get()
                obj.progress = column[6]
                obj.final = bool(column[7])
                obj.comments = column[8]
                experimental_results = {}
                for n, result_name in enumerate(results_names):
                    experimental_results[result_name] = float(column[9+n])
                obj.experimental_results = experimental_results
                obj.save()
            except Experiment.DoesNotExist:
                Experiment.objects.create(
                    compound=Compound.objects.get(name=column[0]),
                    experiment_date=datetime.strptime(column[2], '%Y-%m-%d').date(),
                    experimental_set=exp_set_obj,
                    aparat=Aparat.objects.get(name=column[4]),
                    lab_person=LabPerson.objects.get(name=column[5]),
                    progress=column[6],
                    final=bool(column[7]),
                    comments=column[8]
                )
    return render(
        request,
        "experiments/upload_experiments.html",
        {}
    )



experimental_results={
    'Sp': 0,
    'HyWi': 0,
    'ARR': 0,
    'GSTS2i': 0,
    'MLOGP': 0,
    'Eta_beta': 0,
}