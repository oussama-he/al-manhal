from django import forms
from django.db.models import Q
from taggit.models import Tag

from projects.models import Project, Membership
from .models import Publication, Comment, Rating


class ResourceForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        # todo: revise this, project must be active and user also
        # member_project = ProjectMembers.objects.filter(user__username=user, active=True)
        projects = Project.objects.filter(Q(created_by=user) | Q(members__id__in=[user.id]), active=True).distinct()
        self.fields['project'] = forms.ModelChoiceField(
            queryset=projects,
            widget=forms.Select,
            label="Projet",
        )

    date = forms.DateField(widget=forms.DateInput(format=('%d-%m-%Y')), required=False)

    class Meta:
        model = Publication
        fields = ['title', 'content', 'project', 'source', 'source_url', 'tags', 'contributor', 'coverage', 'creator', 'date',
                  'description', 'format', 'identifier', 'publisher', 'relation', 'rights', 'type', 'language', 'subject'
                  ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'content': forms.Textarea(attrs={'rows': 2}),
            'rights': forms.Textarea(attrs={'rows': 2}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            # 'source_url': forms.URLField(attrs={'type': 'date'})

        }
        help_texts = {
            "tags": "Une liste de mots-clés séparés par des virgules."
        }
        labels = {
            "tags": "Mots-clés"
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content', ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1, 'placeholder': 'Votre Commentaire Ici'}),
        }
        labels = {
            'content': '',
        }


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ['user', 'publication', 'rating', ]


class TagsForm(forms.Form):
    def __init__(self, *args, tags, **kwargs):
        super(TagsForm, self).__init__(*args, **kwargs)
        self.fields['filter_tags'].queryset = tags

    filter_tags = forms.ModelMultipleChoiceField(
        label="Tags",
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        error_messages={"invalid_choice": "Sélectionnez un choix valide, votre choix n'est pas disponible"}
    )


class FilterProjectForm(forms.Form):
    def __init__(self, *args, projects, **kwargs):
        super(FilterProjectForm, self).__init__(*args, **kwargs)
        self.fields['filter_projects'].queryset = projects

    filter_projects = forms.ModelMultipleChoiceField(
        label="Projets",
        queryset=Project.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        error_messages={"invalid_choice": "Sélectionnez un choix valide, votre choix n'est pas disponible"}
    )
