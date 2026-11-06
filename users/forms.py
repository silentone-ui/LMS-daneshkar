from django import forms


class UsersForm(forms.Form):

    email = forms.EmailField(label="ایمیل")
