import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm, RegisterForm, TaskForm
import time

API_AUTH_URL = "http://auth:8000/api/"
API_TASKS_URL = "http://tasks:8000/api/tasks/"  # Изменен порт на 8000


def get_auth_header(request):
    token = request.session.get('jwt_token')
    return {'Authorization': f'Bearer {token}'} if token else {}


def make_api_request(url, method='get', headers=None, data=None, max_retries=3):
    for attempt in range(max_retries):
        try:
            if method == 'get':
                response = requests.get(url, headers=headers)
            elif method == 'post':
                response = requests.post(url, headers=headers, data=data)
            elif method == 'patch':
                response = requests.patch(url, headers=headers, data=data)
            elif method == 'delete':
                response = requests.delete(url, headers=headers)

            return response
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                time.sleep(1 * (attempt + 1))
                continue
            raise
    return None


def login_view(request):
    if request.session.get('jwt_token'):
        return redirect('tasks')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                response = make_api_request(
                    f"{API_AUTH_URL}login/",
                    method='post',
                    data={
                        'username': form.cleaned_data['username'],
                        'password': form.cleaned_data['password']
                    }
                )
                if response and response.status_code == 200:
                    request.session['jwt_token'] = response.json()['access']
                    messages.success(request, "Вы успешно вошли в систему")
                    return redirect('tasks')
                messages.error(request, "Неверные учетные данные")
            except Exception as e:
                messages.error(request, f"Ошибка сервера: {str(e)}")
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})


@csrf_exempt
def tasks_view(request):
    if not request.session.get('jwt_token'):
        return redirect('login')

    headers = get_auth_header(request)
    error = None

    try:
        if request.method == 'POST':
            if 'delete' in request.POST:
                make_api_request(
                    f"{API_TASKS_URL}{request.POST['delete']}/",
                    method='delete',
                    headers=headers
                )
                messages.success(request, "Задача успешно удалена")
            else:
                form = TaskForm(request.POST)
                if form.is_valid():
                    task_data = {
                        'title': form.cleaned_data['title'],
                        'status': form.cleaned_data['status']
                    }
                    if 'task_id' in request.POST:
                        make_api_request(
                            f"{API_TASKS_URL}{request.POST['task_id']}/",
                            method='patch',
                            headers=headers,
                            data=task_data
                        )
                        messages.success(request, "Задача обновлена")
                    else:
                        make_api_request(
                            API_TASKS_URL,
                            method='post',
                            headers=headers,
                            data=task_data
                        )
                        messages.success(request, "Задача создана")
            return redirect('tasks')

        response = make_api_request(API_TASKS_URL, headers=headers)
        if response:
            tasks = response.json() if response.status_code == 200 else []
        else:
            tasks = []
            error = "Сервис задач временно недоступен"

    except Exception as e:
        tasks = []
        error = f"Ошибка при получении задач: {str(e)}"

    return render(request, 'main/tasks.html', {
        'tasks': tasks,
        'form': TaskForm(),
        'error': error
    })

def register_view(request):
    if request.session.get('jwt_token'):
        return redirect('tasks')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['password_confirm']:
                messages.error(request, "Пароли не совпадают")
            else:
                try:
                    response = make_api_request(
                        f"{API_AUTH_URL}register/",
                        method='post',
                        data={
                            'username': form.cleaned_data['username'],
                            'password': form.cleaned_data['password']
                        }
                    )
                    if response and response.status_code == 201:
                        messages.success(request, "Регистрация успешна! Войдите в систему")
                        return redirect('login')
                    error_msg = response.json().get('detail', 'Ошибка регистрации') if response else 'Сервис недоступен'
                    messages.error(request, error_msg)
                except Exception as e:
                    messages.error(request, f"Ошибка сервера: {str(e)}")
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def logout_view(request):
    request.session.flush()
    messages.success(request, "Вы успешно вышли из системы")
    return redirect('login')


def home_view(request):
    username = None

    return render(request, 'main/home.html', {
    })