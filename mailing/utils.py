from django.core.exceptions import EmptyResultSet, PermissionDenied


class ControlUserObject:

    def get_queryset(self):
        """
        Функция возвращает объекты в зависимости от пользователя в запросе
        """
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user).order_by('pk').reverse()

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
