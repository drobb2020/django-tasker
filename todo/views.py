from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.shortcuts import redirect, render

from .forms import CreateUserForm, LoginForm, TaskForm, UpdateProfileForm, UpdateTaskForm
from .models import Task


def index(request):
    """
    This is the root of the site. It renders the index.html template
    with an empty context.

    :param request: The request object
    :return: The rendered index.html template
    """
    context = {}
    return render(request, "todo/index.html", context)


@login_required()
def task_create(request):
    """
    This view is responsible for creating a new task.

    It renders the task_create.html template with a TaskForm
    instance. If the request method is POST, it validates the
    form and saves it to the database. The author of the task is
    set to the current user. After saving the task, it redirects
    to the dashboard.

    :param request: The request object
    :return: The rendered task_create.html template or a redirect to the dashboard
    """
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            messages.success(request, "Your task was successfully created.")
            return redirect("dashboard")

    context = {"form": form}
    return render(request, "todo/task_create.html", context)


@login_required()
def task_detail(request, pk):
    """
    This view is responsible for showing a single task.

    It renders the task_detail.html template with the task
    instance as a context variable.

    :param request: The request object
    :param pk: The id of the task to show
    :return: The rendered task_detail.html template
    """
    task = Task.objects.get(id=pk)
    context = {"task": task}
    return render(request, "todo/task_detail.html", context)


@login_required()
def task_update(request, pk):
    """
    This view is responsible for updating a task.

    It renders the task_update.html template with a UpdateTaskForm
    instance. If the request method is POST, it validates the
    form and saves it to the database. After saving the task, it
    redirects to the dashboard.
    """
    task = Task.objects.get(id=pk)
    form = UpdateTaskForm(instance=task)
    if request.method == "POST":
        form = UpdateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Your task was successfully updated.")
            return redirect("dashboard")
    context = {"task": task, "form": form}
    return render(request, "todo/task_update.html", context)


@login_required()
def task_delete(request, pk):
    """
    This view is responsible for deleting a task.

    It renders the task_delete.html template with the task
    instance as a context variable. If the request method is POST,
    the task is deleted from the database, a success message is
    displayed, and the user is redirected to the dashboard.

    :param request: The request object
    :param pk: The id of the task to delete
    :return: The rendered task_delete.html template or a redirect to the dashboard
    """

    task = Task.objects.get(id=pk)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Your task was successfully deleted.")
        return redirect("dashboard")
    context = {"task": task}
    return render(request, "todo/task_delete.html", context)


@login_required()
def profile(request):
    """
    This view is responsible for displaying the user's profile.

    It renders the profile.html template with the user's profile
    information as a context variable.

    :param request: The request object
    :return: The rendered profile.html template
    """

    context = {"profile": profile}
    return render(request, "todo/profile.html", context)


@login_required()
def profile_update(request):
    """
    This view is responsible for updating the user's profile.

    It renders the profile_update.html template with a UpdateProfileForm
    instance. If the request method is POST, it validates the
    form and saves it to the database. After saving the profile, it
    redirects to the user's profile page.

    :param request: The request object
    :return: The rendered profile_update.html template or a redirect to the profile
    """
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save
            messages.success(request, "Your profile was successfully updated.")
            return redirect("profile")
    else:
        form = UpdateProfileForm(instance=request.user.profile)
    context = {"form": form}
    return render(request, "todo/profile_update.html", context)


def profile_delete(request):
    """
    This view is responsible for deleting the user's profile.

    It renders the profile_delete.html template. If the request
    method is POST, the user's profile is deleted from the
    database, a success message is displayed, and the user is
    redirected to the homepage.

    :param request: The request object
    :return: The rendered profile_delete.html template or a redirect to the homepage
    """
    if request.method == "POST":
        request.user.profile.delete()
        messages.success(request, "Your profile was successfully deleted.")
        return redirect("dashboard")
    return render(request, "todo/profile_delete.html")


@login_required()
def dashboard(request):
    """
    This view is responsible for showing the user's dashboard.

    It renders the dashboard.html template with all the tasks
    created by the user as a context variable.

    :param request: The request object
    :return: The rendered dashboard.html template
    """
    tasks = Task.objects.filter(author=request.user).order_by('-id')
    context = {"tasks": tasks}
    return render(request, "todo/dashboard.html", context)


def register(request):
    """
    This view is responsible for handling user registration.

    It renders the register.html template with a CreateUserForm
    instance. If the request method is POST, it validates the
    form and saves it to the database. After saving the user, it
    redirects to the login page.

    :param request: The request object
    :return: The rendered register.html template or a redirect to the login page
    """
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Registered successfully, please login to get started."
            )
            return redirect("login")

    context = {"form": form}
    return render(request, "todo/register.html", context)


def my_login(request):
    """
    This view is responsible for handling user login.

    It renders the my-login.html template with a LoginForm
    instance. If the request method is POST, it validates the
    form and authenticates the user. If the authentication was
    successful, it logs the user in, displays a success message,
    and redirects to the homepage.

    :param request: The request object
    :return: The rendered my-login.html template or a redirect to the homepage
    """
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect("home")
    context = {"form": form}
    return render(request, "todo/my-login.html", context)


def my_logout(request):
    """
    This view is responsible for handling user logout.

    It logs the user out, displays an information message,
    and redirects to the homepage.

    :param request: The request object
    :return: A redirect to the homepage
    """
    logout(request)
    messages.info(request, "User was successfully logged out")
    return redirect("home")


def about(request):
    """
    This view is responsible for showing the about page.

    It renders the about.html template without any context variables.

    :param request: The request object
    :return: The rendered about.html template
    """
    context = {}
    return render(request, "todo/about.html", context)


def contact(request):
    """
    This view is responsible for showing the contact page.

    It renders the contact.html template without any context variables.

    :param request: The request object
    :return: The rendered contact.html template
    """
    context = {}
    return render(request, "todo/contact.html", context)
