import csv
from datetime import datetime
import io

from django.contrib import messages
from django.shortcuts import render

from .filters import ExperimentFilter, CompoundFilter
from .forms import ExperimentForm, ResultForm, CompoundForm
from .models import Experiment, Result, Compound, Project, ExperimentalSet, \
 Aparat, LabPerson, Experiment_Sp, Experiment_ARR, Experiment_MLOGP  #ExperimentType


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
    compound_instance = Compound.objects.get(compound_name=compound_id)
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
    compound_atrributes = [
        "compound_name",
        "compound_mass",
        "compound_monoisotopic_mass",
        "compound_formula",
        "comments",
        "project"
        ]
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        try:
            obj = Compound.objects.get(compound_name=column[0])
            for atrr_num in range(1, 5):
                setattr(obj, compound_atrributes[atrr_num], column[atrr_num])
            setattr(obj, compound_atrributes[5], Project.objects.filter(project_name=column[5])[0])
            obj.save()
        except Compound.DoesNotExist:
            Compound.objects.create(
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


def experiments_upload(request):
    if request.method == "GET":
        return render(request, "experiments/upload_experiments.html", {})
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        if column[1] == "Sp":
            Exp = Experiment_Sp
        if column[1] == "ARR":
            Exp = Experiment_ARR
        if column[1] == "MLOGP":
            Exp = Experiment_MLOGP
        try:
            exp_set_obj = ExperimentalSet.objects.get(set_name=column[3])
        except ExperimentalSet.DoesNotExist:
            exp_set_obj = ExperimentalSet.objects.create(set_name=column[3], experiment_date=datetime.strptime(column[2], '%Y-%m-%d').date())
        try:
            obj = Exp.objects.get(
                compound=Compound.objects.get(compound_name=column[0]),
                experimental_set=exp_set_obj
                )
            setattr(obj, 'experiment_date', datetime.strptime(column[2], '%Y-%m-%d').date())
            setattr(obj, 'aparat', Aparat.objects.filter(aparat_name=column[4]))
            setattr(obj, 'lab_person', LabPerson.objects.filter(lab_name=column[5]))
            setattr(obj, 'progress', column[6])
            setattr(obj, 'final', bool(column[7]))
            setattr(obj, 'comments', column[8])
            obj.save()
        except Experiment.DoesNotExist:
            Exp.objects.create(
                compound=Compound.objects.get(compound_name=column[0]),
                experiment_date=datetime.strptime(column[2], '%Y-%m-%d').date(),
                experimental_set=exp_set_obj,
                aparat=Aparat.objects.get(aparat_name=column[4]),
                lab_person=LabPerson.objects.get(lab_name=column[5]),
                progress=column[6],
                final=bool(column[7]),
                comments=column[8]
            )
    return render(
        request,
        "experiments/upload_experiments.html",
        {}
    )


def experiments_upload_with_Sp_results(request):
    if request.method == "GET":
        return render(request, "experiments/upload_experiments.html", {})
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            obj = Experiment_Sp.objects.get(
                compound=Compound.objects.get(compound_name=column[0]),
                experimental_set=ExperimentalSet.objects.get(set_name=column[3])
                )
            setattr(obj, 'comments', column[8])
            setattr(obj, 'result_Sp', column[9])
            setattr(obj, 'result_HyWi', column[10])
            obj.save()
    return render(
        request,
        "experiments/upload_experiments.html",
        {}
    )


def experiments_upload_with_ARR_results(request):
    if request.method == "GET":
        return render(request, "experiments/upload_experiments.html", {})
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            obj = Experiment_ARR.objects.get(
                compound=Compound.objects.get(compound_name=column[0]),
                experimental_set=ExperimentalSet.objects.get(set_name=column[3])
                )
            setattr(obj, 'comments', column[8])
            setattr(obj, 'result_ARR', column[9])
            setattr(obj, 'result_GSTS2i', column[10])
            obj.save()
    return render(
        request,
        "experiments/upload_experiments.html",
        {}
    )


def experiments_upload_with_MLOGP_results(request):
    if request.method == "GET":
        return render(request, "experiments/upload_experiments.html", {})
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            obj = Experiment_MLOGP.objects.get(
                compound=Compound.objects.get(compound_name=column[0]),
                experimental_set=ExperimentalSet.objects.get(set_name=column[3])
                )
            setattr(obj, 'comments', column[8])
            setattr(obj, 'result_MLOGP', column[9])
            setattr(obj, 'result_Eta_beta', column[10])
            obj.save()
    return render(
        request,
        "experiments/upload_experiments.html",
        {}
    )
