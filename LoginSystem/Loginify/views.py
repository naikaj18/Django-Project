from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import UserDetails  # Import your UserDetails model

def home(request):
    return HttpResponse("Hello world!")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if the email is unique
        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken.")
            return redirect('signup')

        # Save the user data
        user = UserDetails(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Signup successful! You can now login.")
        return redirect('login')
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Check if a user with the provided email and password exists
        try:
            user = UserDetails.objects.get(email=email, password=password)
            messages.success(request, f"Welcome, {user.username}!")
            return render(request, 'success.html', {'user': user})
        except UserDetails.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')