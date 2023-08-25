from django import forms


class new_a(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    price = forms.IntegerField(required=True)
    location = forms.CharField(required=True)
    work_zone = forms.BooleanField(required=False)
    number_of_rooms = forms.IntegerField(required=True)
    number_of_bedrooms = forms.IntegerField(
        required=True)
    space_for_people = forms.IntegerField(required=True)
    images = forms.ImageField(required=True)


class log_in(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())


class sign_up(forms.Form):
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
