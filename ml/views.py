
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ml.forms import MLAlgorithmForm

@login_required
def add_algorithm(request):
    if request.method == 'POST':
        form = MLAlgorithmForm(request.POST)
        if form.is_valid():
            #form.save(commit=False)
            alg = form.save(commit=False)
            model = request.FILES["joblib_binary_file_algorithm"].read()
            encoder = request.FILES["joblib_binary_file_encoders"].read()
            alg.joblib_binary_file_algorithm = model
            alg.joblib_binary_file_encoders = encoder
            alg.save()
            return redirect('ml:add_ml_algorithm')
    else:
        form = MLAlgorithmForm()

    return render(request, 'ml/add_ml_algorithm.html', {'form': form})




