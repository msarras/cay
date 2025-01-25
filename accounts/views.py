# accounts/views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserUpdateForm


class ProfileView(LoginRequiredMixin, View):
    template = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        form = UserUpdateForm(instance=user)  # Pre-fill the form with the user's current data
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Save the updated user information
            return HttpResponseRedirect(request.path_info)  # Redirect to the same page to show updated info
        return render(request, self.template, {'form': form})
