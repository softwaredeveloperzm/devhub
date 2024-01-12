from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import UserUpdateForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError



 #Use this decorator to exempt CSRF token requirement for simplicity. Be cautious in production.
@csrf_exempt 
def signup(request):
    if request.method == 'POST':
        # Retrieve form data
        full_names = request.POST.get('full_names')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Check if the user with the given email already exists
            user = User.objects.get(username=email)
            return JsonResponse({'error': 'User with this email already exists. Please log in.'})

        except User.DoesNotExist:
            # Create a new user
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = full_names
            user.save()

            # Log in the user
            login(request, user)

            return JsonResponse({'success': 'User registered successfully'})

        except IntegrityError:
            # Handle any other IntegrityError that might occur
            return JsonResponse({'error': 'An error occurred during signup. Please try again.'})

    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        # Retrieve form data
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember', False)

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Log in the user
            login(request, user)

            # Set session expiry for "Remember me" functionality
            if not remember_me:
                request.session.set_expiry(0)

            # Return success JSON response
            return JsonResponse({'success': True})
        else:
            # Return error JSON response
            return JsonResponse({'success': False, 'error': 'Invalid email or password. Please try again.'})

    # Return error JSON response for invalid request method
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("/")



def home(request):

    return render(request, 'users/home.html')



def profile(request, email):
    user = get_user_model().objects.filter(username=email).first()
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            new_email = form.cleaned_data['email']
            if user.email != new_email:
                # Change the user's email and save the user model
                user.email = new_email
                user.save()
                
            # Save the form changes
            form.save()

            # Redirect to the updated profile page or any other appropriate view
            return redirect('profile', email=new_email)
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'users/insite/profile.html', context={'form': form})



