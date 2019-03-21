import json

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from accounts.models import User
from portal.forms import ResourceForm
from portal.models import Publication
from projects.forms import SecondaryObjectiveForm, ProjectForm
from projects.models import Project, SecondaryObjective
from .forms import SignUpForm, EditProfileForm, UserAvatarForm, SignInForm


def sidebar(request):
    return render(request, 'accounts/login.html', {})

def check_status(request):
    if request.user.is_authenticated():
        return HttpResponse("<p>User is auth</p>")
    else:
        return HttpResponse("<p>user isn't auth")

def sign_in_view(request):
    if request.method == 'POST':
        sign_in_form = SignInForm(request.POST)

        if sign_in_form.is_valid():
            username = sign_in_form.cleaned_data.get('username')
            password = sign_in_form.cleaned_data.get('password')
            if User.objects.filter(username=username).exists():
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({"status": "ok"}, safe=False, status=200)
                elif user is None:
                    data = {
                        "password": [
                            {
                                "message": "nom d'utilisateur ou mot de passe incorrect",
                                "code": "incorrect"
                            }
                        ],
                        "username": [
                            {
                                "message": "nom d'utilisateur ou mot de passe incorrect",
                                "code": "incorrect"
                            }
                        ]
                    }
                    data = json.dumps(data)
                    return JsonResponse(data, safe=False, status=400)
                else:
                    data = {
                        "password": [
                            {
                            "message": "nom d'utilisateur ou mot de passe incorrect",
                            "code": "incorrect"
                            }
                        ],
                        "username": [
                            {
                                "message": "nom d'utilisateur ou mot de passe incorrect",
                                "code": "incorrect"
                            }
                        ]
                    }
                    data = json.dumps(data)
                    return JsonResponse(data, safe=False, status=400)

            else:
                data = {
                    "password": [
                        {
                            "message": "nom d'utilisateur ou mot de passe incorrect",
                            "code": "incorrect"
                        }
                    ],
                    "username": [
                        {
                            "message": "nom d'utilisateur ou mot de passe incorrect",
                            "code": "incorrect"
                        }
                    ]
                }
                data = json.dumps(data)
                return JsonResponse(data, safe=False, status=400)
        else:
            data = sign_in_form.errors.as_json()
            return JsonResponse(data, safe=False, status=400)
    return HttpResponse("A problem")


def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(request, user)
            return JsonResponse({"status": "ok"}, safe=False, status=200)
        else:
            data = form.errors.as_json()
            return JsonResponse(data, safe=False, status=400)

    else:
        return HttpResponse("A problem in sign up view")

@login_required
def overview(request, username):
    SecondaryObjectiveFormSet = inlineformset_factory(Project, SecondaryObjective, form=SecondaryObjectiveForm,
                                                      extra=3, can_delete=False)
    user = User.objects.get(username=username)
    projects = Project.objects.filter(Q(created_by=user) | Q(members__id__in=[user.id]), active=True).distinct()
    resources = Publication.objects.filter(project__in=projects, user=user, archived=False)
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        objectives_formset = SecondaryObjectiveFormSet(request.POST)

        # if project_form.is_valid() and objectives_formset.is_valid():
        #     project = project_form.save(commit=False)
        #     objectives = objectives_formset.save(commit=False)
        #     project.created_by = request.user
        #     project.save()
        #     for objective in objectives:
        #         objective.project = project
        #         objective.save()
        #
        # else:
        #     data = project_form.errors.as_json()
        #     print("form is not valid", data)
        #     return JsonResponse(data, safe=False, status=400)
    else:
        objectives_formset = inlineformset_factory(Project, SecondaryObjective, form=SecondaryObjectiveForm,
                                                          extra=3, can_delete=False,)
        # objectives_formset = objectives_formset(initial=SecondaryObjective.objects.all().values())
        objectives_formset = objectives_formset()
        project_form = ProjectForm()

    return render(request, 'accounts/profile-overview.html', {
        'user': user,
        "resources": resources,
        "projects": projects,
        "form": ResourceForm(user=request.user),
        "project_form": project_form,
        "objectives_formset": objectives_formset,
    })


@login_required
def edit_profile(request, username):
    user = User.objects.get(username=username)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            user_profile = form.save(commit=False)

            if 'picture' in request.FILES:
                user_profile.avatar = request.FILES['picture']

            user_profile.save()
            return redirect("accounts:edit-profile", username=request.user.username)
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'accounts/edit-profile.html', {'form': form})


@login_required
def change_user_avatar(request):
    if request.method == 'POST':
        profile_form = UserAvatarForm(request.POST, request.FILES, instance=request.user)

        if profile_form.is_valid():

            profile = profile_form.save(commit=False)
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            profile.save()
            return redirect("accounts:edit-profile", username=request.user.username)


def logout_view(request):
    logout(request)
    return redirect("portal:home")
