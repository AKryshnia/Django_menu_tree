from django.views.generic import TemplateView


class MenuView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_name = self.kwargs.get('menu_name') or 'main_menu'
        context['menu_name'] = menu_name
        return context
