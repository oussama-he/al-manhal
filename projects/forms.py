from django import forms
from django.contrib.admin import widgets

from accounts.models import User
from projects.models import Project, SecondaryObjective


class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        # todo get active users only
        # members = User.objects.all()
        # self.fields['project'] = forms.ModelMultipleChoiceField(
        #     queryset=members,
        #     widget=forms.CheckboxSelectMultiple,
        #     # todo change required to false
        #     required=False
        # )
    #     todo return active users only
    members = forms.ModelMultipleChoiceField(
        label="Members",
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Project
        fields = ['title', 'description', 'objective', 'duration', 'members']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, }),
            'objective': forms.Textarea(attrs={'rows': 2}),
            # 'duration': forms.DateInput(),
        }
        labels = {
            "title": "Nom de Projet",
            "objective": "Objectiif global & Objectiifs secondaires",
            "duration": "Durée"
        }


class SecondaryObjectiveForm(forms.ModelForm):

    class Meta:
        model = SecondaryObjective
        fields = ['objective', ]
        labels = {
            "objective": "Objective Secondaire"
        }


