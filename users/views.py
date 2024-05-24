import secrets

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.core.exceptions import PermissionDenied

from config import settings
from mailing.models import Mailing
from users.forms import UserAuthenticationForm, UserRegistrationForm, UserUserChangeForm
from users.models import User


class Login(LoginView):
    """
    Представление - это вызываемый объект, который принимает запрос и возвращает ответ
    Представление авторизации пользователей
    """

    template_name = "users/login.html"
    form_class = UserAuthenticationForm
    extra_context = {"title": "Вход на сайт", "description": "Введите вашу электронную почту и пароль для авторизации"}


class Logout(LoginRequiredMixin, LogoutView):
    """
    Представление выхода пользователей
    """

    pass


class UserRegisterView(CreateView):
    """
    Представление регистрации пользователей
    """

    model = User
    form_class = UserRegistrationForm
    template_name = "users/register.html"
    extra_context = {"title": "Регистрация", "description": "Введите ваши данные для регистрации на сайте"}

    def form_valid(self, form):
        """
        Функция проверки валидности формы
        :param form: форма
        :return: HttpResponseRedirect
        """
        new_user = form.save()
        new_user.is_active = False
        token = secrets.token_hex(16)
        new_user.token = token
        new_user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/success_email_confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Перейдите по ссылки для подтверждения почты {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
        )

        return super().form_valid(form)

    def get_success_url(self):
        """
        Функция возврата url представления подтверждения электронной почты
        :return: url
        """
        return reverse_lazy("users:email_confirm", args=[self.request.POST.get("email")])


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление редактирования пользователей(в данном случае является и детальным просмотром пользователя,
    т.е. профилем пользователя)
    """

    model = User
    success_url = reverse_lazy("users:profile")
    form_class = UserUserChangeForm

    def get_object(self, queryset=None):
        """
        Функция возврата объекта, который будет отображаться в этом представлении
        :param queryset: None
        :return: user
        """
        return self.request.user


def email_confirm(request, email):
    """
    Функция представления подтверждения электронной почты
    :param request: request
    :param email: User.email
    :return: HTTPResponse
    """
    context = {
        "title": "Подтверждение электронной почты",
        "description": "Необходимо подтвердить электронную почту для входа на сайт",
        "message": f"На вашу электронную почту {email} направлено письмо с ссылкой для подтверждения. "
        f"Войдите в вашу электронную почту и перейдите по ссылке, что указано в письме",
    }
    return render(request, "users/email_confirm.html", context)


def success_email_confirm(request, token: str):
    """
    Функция представления успешного подтверждения электронной почты
    :param request: request
    :param token: User.token
    :return: HTTPResponse
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    send_mail(
        subject="Поздравляем с регистрацией",
        message="Вы зарегистрировались на нашей платформе. Добро пожаловать!",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )
    context = {
        "title": "Успешное подтверждение электронной почты",
        "description": "Вы подтвердили регистрацию, и теперь можете войти",
        "message": "Добро пожаловать на сайт!",
    }
    return render(request, "users/email_confirm.html", context)


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = "users.view_user"
    extra_context = {"title": "Просмотр пользователей", "description": "В таблице отображаются все пользователи"}

    def get_queryset(self):
        """
        Функция возвращает объекты User
        """
        queryset = super().get_queryset()
        return queryset.all().order_by("pk").reverse()


@permission_required(["users.view_user", "users.change_active"], login_url=reverse_lazy("users:user_list"))
@login_required
def user_set_active(request, pk):
    """
    Функция блокировки и разблокировки пользователей сайта
    :param pk:
    """
    user = get_object_or_404(User, pk=pk)
    if not user.is_superuser:
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
    return redirect(reverse("users:user_list"))


@login_required
def mailing_set_active(request, pk):
    """
    Функция блокировки и разблокировки пользователей сайта
    :param pk:
    """
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.owner == request.user or request.user.is_staff:
        if mailing.is_active:
            mailing.is_active = False
        else:
            mailing.is_active = True
        mailing.save()
    else:
        raise PermissionDenied("Доступ запрещен")
    return redirect(reverse("mailing:mailing_list"))
