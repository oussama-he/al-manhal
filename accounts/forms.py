from django import forms
from .models import User
from portal.models import Publication


class SignInForm(forms.Form):
    username = forms.CharField(required=True, label="Nom d'utilisateur", help_text="")
    password = forms.CharField(required=True, label="Mot de Passe", widget=forms.PasswordInput)


class SignUpForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(label="Mot de Passe", required=True, widget=forms.PasswordInput)
    first_name = forms.CharField(label="Nom")
    last_name = forms.CharField(label="Prenom")
    confirm_password = forms.CharField(label="Confirmez le mot de passe", widget=forms.PasswordInput)
    email = forms.EmailField(required=True, label="Adresse mail")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'username': "Nom d'utilisateur",
            'password': "Mot de Passe",
            "first_name": "Nom",
            "last_name": "Prenom"
        }
        help_texts = {
            "username": "150 caractères ou moins. Lettres, chiffres et @ /. / + / - / _ seulement."
        }

    # def clean_password(self):
    #     cleaned_data = super(SignUpForm, self).clean()
    #
    #     password = cleaned_data.get('password')
    #     password_confirm = cleaned_data.get('confirm_password')
    #
    #     if password and password_confirm:
    #         if password != password_confirm:
    #             raise forms.ValidationError("Les deux champs de mot de passe doivent correspondre.")
    #     return cleaned_data

    # def clean_confirm_password(self):
    #     cleaned_data = super(SignUpForm, self).clean()
    #
    #     password = cleaned_data.get('password')
    #     password_confirm = cleaned_data.get('confirm_password')
    #
    #     if password and password_confirm:
    #         if password != password_confirm:
    #             raise forms.ValidationError("Les deux champs de mot de passe doivent correspondre.")
    #     return cleaned_data


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            "first_name": "Nom",
            "last_name": "Prenom",
            'email': "Adresse mail",
        }


class UserAvatarForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['avatar', ]
