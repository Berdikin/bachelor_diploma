from django.conf import settings


menu = [
    {'title': 'Главная', 'url_name': 'home', 'icon': 'fas fa-home'},
    {'title': 'Расписание', 'url_name': 'timetable', 'icon': 'fas fa-calendar'},
    {'title': 'Отзывы', 'url_name': 'reviews', 'icon': 'fas fa-comments'},
    {'title': 'Журналы', 'url_name': 'logs', 'icon': 'fas fa-book-open'}
]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(-1)
            user_menu.pop(-1)
        context['menu'] = user_menu
        return context

