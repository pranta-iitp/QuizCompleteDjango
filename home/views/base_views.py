from django.shortcuts import render, redirect
import json
from django.contrib import messages
# if we give only .models, it seraches in the same folder
from ..models import User, Author, Participant
from ..models import generate_user_id  # Make sure it's defined in models.py
from django.urls import reverse
from django.db import IntegrityError

def home(request):
    peoples = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
        {"name": "Charlie", "age": 22},
    ]
    # Pass as a JSON string
    return render(request, "home/index.html", {"peoples": json.dumps(peoples)})

def author_signup(request):
    if request.method == 'POST':
        data = request.POST
        user_id = generate_user_id()

        # Check for duplicates

        if User.objects.filter(user_name=data['user_name']).exists() and User.objects.filter(user_email=data['user_email']).exists():
            return redirect(f"{reverse('author_signup')}?error=already_exists")

        if User.objects.filter(user_name=data['user_name']).exists():
            return redirect(f"{reverse('author_signup')}?error=username_taken")

        if User.objects.filter(user_email=data['user_email']).exists():
            return redirect(f"{reverse('author_signup')}?error=email_taken")

        try:
            user = User.objects.create(
                user_id=user_id,
                user_name=data['user_name'],
                user_password=data['user_password'],
                user_email=data['user_email'],
                user_role='author',
                user_status='active'
            )

            Author.objects.create(
                author_id=generate_user_id(),
                author_user=user,
                author_name=data['user_name'],
                author_email=data['user_email'],
                author_full_name='',
                author_subject_a='',
                author_subject_b='',
                author_subject_c='',
                author_subject_d='',
            )

            return redirect(f"{reverse('author_signup')}?success=1")

        except Exception as e:
            return redirect(f"{reverse('author_signup')}?error=registration_failed")

    return render(request, "home/author_signup.html")


def participant_join(request):
    if request.method == 'POST':
        data = request.POST
        user_id = generate_user_id()

        # Check for duplicates

        if User.objects.filter(user_name=data['user_name']).exists() and User.objects.filter(user_email=data['user_email']).exists():
            return redirect(f"{reverse('participant_join')}?error=already_exists")

        if User.objects.filter(user_name=data['user_name']).exists():
            return redirect(f"{reverse('participant_join')}?error=username_taken")

        if User.objects.filter(user_email=data['user_email']).exists():
            return redirect(f"{reverse('participant_join')}?error=email_taken")

        try:
            user = User.objects.create(
                user_id=user_id,
                user_name=data['user_name'],
                user_password=data['user_password'],
                user_email=data['user_email'],
                user_role='participant',
                user_status='active'
            )

            Participant.objects.create(
                participant_id=generate_user_id(),
                participant_user=user,
                participant_name=data['user_name'],
                participant_email=data['user_email'],
                participant_full_name ='',
                preferred_subject_a='',
                preferred_subject_b='',
                preferred_subject_c='',
                preferred_subject_d='',
            )

            return redirect(f"{reverse('participant_join')}?success=1")

        except Exception as e:
            return redirect(f"{reverse('participant_join')}?error=registration_failed")

    return render(request, "home/participant_join.html")

def show_authors(request):
    authors = Author.objects.all()
    return render(request, "home/authors.html", {"authors": authors})

def sign_in1(request):
    if request.method == 'POST':
        data = request.POST
        username_or_email = data.get('username')
        password = data.get('password')

        user = None

        # Check by email and password
        try:
            user = User.objects.get(user_email=username_or_email, user_password=password)
        except User.DoesNotExist:
            pass

        # If not found, check by username
        if user is None:
            try:
                user = User.objects.get(user_name=username_or_email, user_password=password)
            except User.DoesNotExist:
                pass

        # Invalid credentials
        if user is None:
            return redirect(f"{reverse('sign_in')}?error=invalid_credentials")

        # Check status
        if user.user_status.lower() != 'active':
            return redirect(f"{reverse('sign_in')}?error=inactive_user")

        # Save user_id in session
        request.session['user_id'] = user.user_id

        # Redirect based on role
        if user.user_role.lower() == 'author':
            # Fetch author record
            try:
                author = Author.objects.get(user=user)
                request.session['author_id'] = author.author_id
            except Author.DoesNotExist:
                request.session['author_id'] = None
            return redirect('author_dashboard')

        elif user.user_role.lower() == 'participant':
            return redirect('participant_dashboard')

        else:
            return render(request, "home/sign_in.html")

    # GET request → show login page
    return render(request, "home/sign_in.html")


def sign_in(request):
    if request.method == 'POST':
        data = request.POST
        username_or_email = data.get('username')
        password = data.get('password')

        user = None

        # 🔹 Check by email and password
        try:
            user = User.objects.get(user_email=username_or_email, user_password=password)
        except User.DoesNotExist:
            pass

        # 🔹 If not found, check by username and password
        if user is None:
            try:
                user = User.objects.get(user_name=username_or_email, user_password=password)
            except User.DoesNotExist:
                pass

        # 🔹 If still not found → invalid credentials
        if user is None:
            return redirect(f"{reverse('sign_in')}?error=invalid_credentials")

        # 🔹 Check if user is active
        if user.user_status.lower() != 'active':
            # messages.error(request, "Your account is inactive. Please contact admin.")
            # return render(request, "home/sign_in.html")
            return redirect(f"{reverse('sign_in')}?error=inactive_user")
        # Store user info in session
        request.session['user_id'] = user.user_id
        request.session['user_role'] = user.user_role
        request.session['user_name'] = user.user_name

        if user.user_role.lower() == 'author':
            try:
                author = Author.objects.get(author_user_id=user.user_id)
                request.session['author_id'] = author.author_id
            except Author.DoesNotExist:
                request.session['author_id'] = None
            return redirect('author_dashboard')

        elif user.user_role.lower() == 'participant':
            try:
                participant = Participant.objects.get(participant_user_id=user.user_id)
                request.session['participant_id'] = participant.participant_id
            except Participant.DoesNotExist:
                request.session['participant_id'] = None
            return redirect('participant_dashboard')

        else:
            messages.error(request, "Invalid user role.")
            return render(request, "home/sign_in.html")

    # For GET request, show login page...before signing in
    return render(request, "home/sign_in.html")



def author_dashboard(request):
    user_id = request.session.get('user_id')
    author_id = request.session.get('author_id')
    user_name = request.session.get ('user_name')
    #print('author_id ',author_id)
    # Optional: Fetch author info for display
    author = None
    if author_id:
        author = Author.objects.get(pk=author_id)

    return render(request, "home/author_dashboard.html", {
        'user_id': user_id,
        'author_id': author_id,
        'author': author,
        'user_name':user_name
    })


def participant_dashboard(request):
    return render(request, "home/participant_dashboard.html")

#action="{% url 'update_author_profile' %}"