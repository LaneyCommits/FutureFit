from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'resume_analysis/home.html'
