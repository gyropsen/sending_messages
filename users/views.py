from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import secrets
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from users.forms import UserAuthenticationForm, UserRegistrationForm, UserUserChangeForm
from users.models import User
from config import settings


class Login(LoginView):
    template_name = 'users/login.html'
    form_class = UserAuthenticationForm
    extra_context = {'title': 'Вход на сайт',
                     'description': 'Введите вашу электронную почту и пароль для авторизации'}


class Logout(LoginRequiredMixin, LogoutView):
    pass


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация',
                     'description': 'Введите ваши данные для регистрации на сайте'}

    def form_valid(self, form):
        new_user = form.save()
        new_user.is_active = False
        token = secrets.token_hex(16)
        new_user.token = token
        new_user.save()

        host = self.request.get_host()
        url = f'http://{host}/users/success_email_confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Перейдите по ссылки для подтверждения почты {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:email_confirm', args=[self.request.POST.get('email')])


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserUserChangeForm

    def get_object(self, queryset=None):
        return self.request.user


def email_confirm(request, email):
    context = {'title': 'Подтверждение электронной почты',
               'description': 'Необходимо подтвердить электронную почту для входа на сайт',
               'message': f'На вашу электронную почту {email} направлено письмо с ссылкой для подтверждения. '
                          f'Войдите в вашу электронную почту и перейдите по ссылке, что указано в письме'
               }
    return render(request, 'users/email_confirm.html', context)


def success_email_confirm(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    send_mail(
        subject='Поздравляем с регистрацией',
        message='Вы зарегистрировались на нашей платформе. Добро пожаловать!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )
    context = {'title': 'Успешное подтверждение электронной почты',
               'description': 'Вы подтвердили регистрацию, и теперь можете войти',
               'message': 'Добро пожаловать на сайт!'
               }
    return render(request, 'users/email_confirm.html', context)
