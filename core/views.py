from django.contrib.auth import logout
from django.views.generic import ListView, RedirectView, FormView
from item.models import Category, Item
from .forms import SignupForm
from django.shortcuts import render
from django.urls import reverse_lazy


class IndexView(ListView):
    """
    This will serve as my index view of the website.
    """
    template_name = 'index.html'
    context_object_name = 'items'
    queryset = Item.objects.filter(is_sold=False)[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class FormsView(FormView):
    """
    This class will serve as the signup form model for users
    """
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('core:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


class LogoutView(RedirectView):
    url = reverse_lazy('core:index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
