from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, False)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.phone_number = form.cleaned_data['phone_number']
        user.postal_code = form.cleaned_data['postal_code']
        user.members_per_account = form.cleaned_data['members_per_account']
        if commit:
            user.save()
        return user
