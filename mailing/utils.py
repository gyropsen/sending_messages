from django.core.exceptions import EmptyResultSet, PermissionDenied

from mailing.models import Mailing


class ControlUserObject:
    """
    Класс управления пользовательским объектом в представлениях
    """

    def get_queryset(self):
        """
        Функция возвращает объекты в зависимости от пользователя в запросе
        """
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_staff:
            return queryset.all().order_by("pk").reverse()
        return queryset.filter(owner=user).order_by("pk").reverse()

    def get_object(self):
        """
        Функция возвращает объект в зависимости от пользователя в запросе
        """
        queryset = self.model.objects.filter(pk=self.kwargs.get("pk"))
        if queryset:
            if queryset.filter(owner=self.request.user):
                return queryset.first()
            else:
                raise PermissionDenied("Доступ запрещен")
        raise EmptyResultSet("Запрос не возвращает никаких результатов")


class ConfigForms:
    """
    Класс конфигурирования стиля и цензуры формы
    """

    forbidden_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "is_active":
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class AddArgumentsInForms:
    """
    Класс добавления аргументов в форму
    """

    def get_form_kwargs(self):
        """
        Функция добавления в форму пользователя
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class GetArgumentsInForms:
    """
    Класс получения аргументов в формах
    """

    def __init__(self, *args, user=None, **kwargs):
        """
        Инициализация экземпляра формы с дальнейшим присваиванием полям аргументов
        :param user: Пользователь в представлении
        """
        super().__init__(*args, **kwargs)
        # Если передан user, то присваиваем полю mailing аргументу queryset
        # только принадлежащие user mailing объекты
        if user is not None:
            self.fields["mailing"].queryset = Mailing.objects.filter(owner=user)
