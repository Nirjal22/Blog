from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required

# views.py - Handle the logic for creating, editing, and deleting posts.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from blog_generator.forms import ContactForm
from django.contrib import messages
from .models import Posts

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        author = request.user
        post = Posts.objects.create(title=title, content=content, author=author)
        return redirect('index')  # Redirect to the index page after creating the post
    return render(request, 'create_post.html')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save()
        return redirect('index')  # Redirect to the index page after editing the post
    return render(request, 'edit_post.html', {'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    if post.author == request.user:
        post.delete()
    return redirect('index')  # Redirect to the index page after deleting the post

@login_required
def index(request):
    # Fetch posts created by the currently logged-in user
    posts = Posts.objects.filter(author=request.user).order_by('-date_posted')  # Filter by user

    return render(request, 'index.html', {'posts': posts})


def login_view(request):
    if request.method == 'POST':
        usernameInput = request.POST['username']
        passwordInput = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=usernameInput, password=passwordInput)
        if user is not None:
            # Log the user in
            login(request, user)
            return redirect('/')  # Redirect to the home page
        else:
            # Handle invalid credentials
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        # Match the 'name' attributes from the HTML form
        usernameInput = request.POST['username']  # Use the corrected field name
        passwordInput = request.POST['password']

        # Check if both fields are filled
        if usernameInput and passwordInput:
            try:
                # Create the user
                user = User.objects.create_user(username=usernameInput, password=passwordInput)
                user.save()
                # Log the user in and redirect to the signout page
                login(request, user)
                return redirect('/')  # Ensure 'signout' is defined in urls.py
            except Exception as e:
                # Capture and display any errors during user creation
                error_message = f"Error creating the account: {str(e)}"
                return render(request, 'register.html', {'error_message': error_message})
        else:
            # If fields are missing, return an error message
            error_message = 'Enter valid input'
            return render(request, 'register.html', {'error_message': error_message})

    # Render the registration form if the request is GET
    return render(request, 'register.html')

def signout(request):
    logout(request)
    return redirect('/')  # Redirect to home page after logout


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact_us')  # Redirect to the contact page or another page
    else:
        form = ContactForm()

    return render(request, 'contact_us.html', {'form': form})