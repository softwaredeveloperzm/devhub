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
from django.db import IntegrityError




def signup(request):
    if request.method == 'POST':
        # Retrieve form data
        full_names = request.POST.get('full_names')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Check if the user with the given email already exists
            user = User.objects.get(username=email)
            error_message = 'User with this email already exists. Please log in.'
            return render(request, 'signup.html', {'error_message': error_message})

        except User.DoesNotExist:
            # Create a new user
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = full_names
            user.save()

            # Log in the user
            login(request, user)

            success_message = 'User registered successfully'
            
            return redirect('base:all_questions')
        except IntegrityError:
            # Handle any other IntegrityError that might occur
            error_message = 'An error occurred during signup. Please try again.'
            return render(request, 'users/signup.html', {'error_message': error_message})
        

    # Render the initial signup form
    return render(request, 'users/signup.html')




def signin(request):
    error_message = None

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

            # Render the success HTML file
            return redirect('base:all_questions')
        else:
            # Set an error message
            error_message = 'Invalid email or password. Please try again.'

    # Render the signin HTML file with an optional error message
    return render(request, 'users/login.html', {'error_message': error_message})


def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("base:all_questions")


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
            return redirect('users:profile', email=new_email)
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'users/insite/profile.html', context={'form': form})



