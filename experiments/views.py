import base64
import csv
from datetime import datetime
from io import BytesIO, StringIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from rdkit import Chem
from rdkit.Chem import Draw

from .filters import ExperimentFilter, CompoundFilter
from .forms import ExperimentForm, CompoundForm
from .models import Experiment, Compound, Project, ExperimentalSet, Aparat, LabPerson, ExperimentType


@login_required
def experiments_list_view(request):
    experiment_list = Experiment.objects.all()
    tableFilter = ExperimentFilter(request.GET, queryset=experiment_list)
    context = {"experiments": experiment_list, "tableFilter": tableFilter}
    return render(request, "experiments/experiments_list.html", context)


@login_required
def edit_experiment_view(request, experiment_id):
    experiment_instance = Experiment.objects.get(id=experiment_id)
    if request.method == "POST":
        experiment_form = ExperimentForm(data=request.POST, instance=experiment_instance)
        if experiment_form.is_valid():
            experiment_form.save()
    else:
        experiment_form = ExperimentForm(instance=experiment_instance)
    return render(request, "experiments/edit_experiment.html", {"experiment_form": experiment_form})


@login_required
def results_list_view(request):
    experiment_list = Experiment.objects.all()
    tableFilter = ExperimentFilter(request.GET, queryset=experiment_list)
    context = {"experiments": experiment_list, "tableFilter": tableFilter}
    return render(request, "experiments/results_list.html", context)


@login_required
def compound_list_view(request):
    compound_list = Compound.objects.all()
    compound_smiles = Compound.objects.values_list("smiles", flat=True)
    encoded_images = []
    for smiles in compound_smiles:
        if smiles:
            molecule = Chem.MolFromSmiles(smiles)
            Chem.rdDepictor.Compute2DCoords(molecule)
            tmpfile = BytesIO()
            image = Draw.MolToImage(molecule, size=(150, 150))
            image.save(tmpfile, "PNG")
            encoded_image = base64.b64encode(tmpfile.getvalue()).decode("utf-8")
            tmpfile.close()
            encoded_images.append(encoded_image)
        else:
            encoded_images.append(None)
    tableFilter = CompoundFilter(request.GET, queryset=compound_list)
    context = {"experiments": compound_list, "tableFilter": tableFilter, "encoded_images": encoded_images}
    return render(request, "experiments/compounds_list.html", context)


@login_required
@permission_required("is_staff")
def edit_compound_view(request, compound_id):
    compound_instance = Compound.objects.get(id=compound_id)
    if request.method == "POST":
        compound_form = CompoundForm(data=request.POST, instance=compound_instance)
        if compound_form.is_valid():
            compound_form.save()
    else:
        compound_form = CompoundForm(instance=compound_instance)
    return render(request, "experiments/edit_compound.html", {"compound_form": compound_form})


@login_required
@permission_required('is_staff')
def compounds_upload_view(request):
    if request.method == "POST":
        csv_file = request.FILES["file"]
        if not csv_file.name.endswith(".csv"):
            messages.error(request, "THIS IS NOT A CSV FILE")
        data_set = csv_file.read().decode("UTF-8")
        io_string = StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=",", quotechar="|"):
            try:
                obj = Compound.objects.get(name=column[0])
                obj.mass = column[1]
                obj.monoisotopic_mass = column[2]
                obj.formula = column[3]
                obj.project = column[4]
                obj.comments = column[5]
                if Chem.MolFromSmiles(column[6]):
                    obj.smiles = column[6]
                else:
                    obj.smiles = None
                obj.save()
            except Compound.DoesNotExist:
                if Chem.MolFromSmiles(column[6]):
                    smiles = column[6]
                else:
                    smiles = None
                Compound.objects.create(
                    name=column[0],
                    mass=column[1],
                    monoisotopic_mass=column[2],
                    formula=column[3],
                    comments=column[4],
                    project=Project.objects.filter(name=column[5])[0],
                    smiles=smiles,
                )
        return redirect("experiments:compoundList")
    else:
        return render(request, "experiments/upload_compounds.html", {})


@login_required
def experiments_upload_view(request):
    if request.method == "POST":
        csv_file = request.FILES["file"]
        if not csv_file.name.endswith(".csv"):
            messages.error(request, "THIS IS NOT A CSV FILE")
        data_set = csv_file.read().decode("UTF-8")
        io_string = StringIO(data_set)
        # next(io_string)
        reader = csv.reader(io_string, delimiter=",", quotechar="|")
        first_row = next(reader)
        results_names = [first_row[x] for x in range(9, len(first_row))]
        for n, column in enumerate(reader):
            exp_set_obj = ExperimentalSet.objects.filter(name=column[3]).last()
            if not exp_set_obj:
                exp_set_obj = ExperimentalSet.objects.create(
                    name=column[3], experiment_date=datetime.strptime(column[2], "%Y-%m-%d").date()
                )
            try:
                obj = Experiment.objects.get(
                    compound=Compound.objects.get(name=column[0]), experimental_set=exp_set_obj
                )
                obj.experiment_date = datetime.strptime(column[2], "%Y-%m-%d").date()
                obj.aparat = Aparat.objects.filter(name=column[4]).get()
                obj.lab_person = LabPerson.objects.filter(lab_name=column[5]).get()
                obj.progress = column[6]
                obj.final = bool(column[7])
                obj.comments = column[8]
                obj.exptype = ExperimentType.objects.get(name=column[1])
                experimental_results = {}
                for n, result_name in enumerate(results_names):
                    experimental_results[result_name] = float(column[9 + n])
                obj.experimental_results = experimental_results
                obj.save()
            except Experiment.DoesNotExist:
                Experiment.objects.create(
                    compound=Compound.objects.get(name=column[0]),
                    experiment_date=datetime.strptime(column[2], "%Y-%m-%d").date(),
                    experimental_set=exp_set_obj,
                    aparat=Aparat.objects.get(name=column[4]),
                    exptype=ExperimentType.objects.get(name=column[1]),
                    lab_person=LabPerson.objects.get(lab_name=column[5]),
                    progress=column[6],
                    final=bool(column[7]),
                    comments=column[8],
                )
        return redirect("experiments:experimentList")
    else:
        return render(request, "experiments/upload_experiments.html", {})
