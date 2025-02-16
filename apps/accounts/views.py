# from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from apps.accounts.forms import SignUpForm, SignInForm

def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponse("User Up successfully")
            # return redirect('home')  # Redirect to the homepage after sign-up
    else:
        form = SignUpForm()
    return render(request, 'accounts/sign_up.html', {'form': form})

def sign_in_view(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponse("User login successfully")
            # return redirect('home')  # Redirect to the homepage after sign-in
    else:
        form = SignInForm()
    return render(request, 'accounts/sign_in.html', {'form': form})



