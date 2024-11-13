from django.shortcuts import render, redirect
from django.http import HttpResponse , JsonResponse
from django.contrib import messages
from .models import UserDetails  # Import your UserDetails model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


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

def get_all_users(request):
    users = UserDetails.objects.all()
    users_data = [{"username": user.username, "email": user.email} for user in users]
    return JsonResponse(users_data, safe=False)

def get_user_by_email(request, email):
    try:
        user = UserDetails.objects.get(email=email)
        user_data = {"username": user.username, "email": user.email}
        return JsonResponse(user_data)
    except UserDetails.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

@csrf_exempt
def update_user(request, email):
    if request.method == 'POST':
        try:
            user = UserDetails.objects.get(email=email)
            data = json.loads(request.body)
            user.username = data.get("username", user.username)  # Only update if new data is provided
            user.save()
            return JsonResponse({"message": "User updated successfully"})
        except UserDetails.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def delete_user(request, email):
    if request.method == 'DELETE':
        try:
            user = UserDetails.objects.get(email=email)
            user.delete()
            return JsonResponse({"message": "User deleted successfully"})
        except UserDetails.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)