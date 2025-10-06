from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegistroForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('dashboard')
        else:
            return render(request, 'registration/registro.html', {'form': form})
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})
