from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

class TaskForm(forms.Form):
    title = forms.CharField(
        label='Описание',
        widget=forms.Textarea(attrs={'rows': 3})
    )
    status = forms.ChoiceField(
        label='Статус',
        choices=[
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('done', 'Выполнена')
    ])