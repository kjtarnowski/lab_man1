from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect

from ml.forms import MLAlgorithmForm
from ml.models import MLAlgorithm, MLRequest


@login_required
def ml_algorithm_list_view(request):
    algorithms_list = MLAlgorithm.objects.all()
    context = {"algorithms": algorithms_list}
    return render(request, "ml/ml_algorithms_list.html", context)


@login_required
@permission_required("is_staff")
def add_algorithm_view(request):
    if request.method == "POST":
        form = MLAlgorithmForm(request.POST)
        if form.is_valid():
            alg = form.save(commit=False)
            model = request.FILES["joblib_binary_file_algorithm"].read()
            encoder = request.FILES["joblib_binary_file_encoders"].read()
            alg.joblib_binary_file_algorithm = model
            alg.joblib_binary_file_encoders = encoder
            alg.save()
            return redirect("ml:add_ml_algorithm")
    else:
        form = MLAlgorithmForm()
    return render(request, "ml/add_ml_algorithm.html", {"form": form})


@login_required
@permission_required("is_staff")
def edit_algorithm_view(request, algorithm_id):
    algorithm_instance = MLAlgorithm.objects.get(id=algorithm_id)
    if request.method == "POST":
        form = MLAlgorithmForm(request.POST, instance=algorithm_instance)
        if form.is_valid():
            alg = form.save(commit=False)
            if request.FILES:
                model = request.FILES["joblib_binary_file_algorithm"].read()
                encoder = request.FILES["joblib_binary_file_encoders"].read()
                alg.joblib_binary_file_algorithm = model
                alg.joblib_binary_file_encoders = encoder
            alg.save()
            return redirect("ml:ml_algorithm_list")
    else:
        form = MLAlgorithmForm(instance=algorithm_instance)
    return render(request, "ml/add_ml_algorithm.html", {"form": form})


@login_required
def ml_request_list_view(request):
    ml_request_list = MLRequest.objects.all()
    context = {"ml_requests": ml_request_list}
    return render(request, "ml/ml_request_list.html", context)
