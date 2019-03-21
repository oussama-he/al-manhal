from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import User
from portal.models import Publication
from projects.forms import ProjectForm, SecondaryObjectiveForm
from projects.models import Project, SecondaryObjective, Membership


def manage_group(request):
    SecondaryObjectiveFormSet = inlineformset_factory(Project, SecondaryObjective, form=SecondaryObjectiveForm,
                                                      extra=3, can_delete=False)

    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        objective_formset = SecondaryObjectiveFormSet(request.POST)
        # objective_form = SecondaryObjectiveForm(request.POST)
        if project_form.is_valid() and objective_formset.is_valid():
            project = project_form.save(commit=False)
            objective = objective_formset.save(commit=False)
            print("is valid >>>>>>>", objective)
            project.created_by = request.user
            project.save()
            for obj in objective:
                obj.project = project
                obj.save()
                print("is valid >>>>>>>", obj.objective)

            return redirect("portal:home")
        else:
            data = project_form.errors.as_json()
            print("form is not valid", data)
            return JsonResponse(data, safe=False, status=400)
    else:
        project_form = ProjectForm()
        objective_formset = SecondaryObjectiveFormSet()

    return render(request, 'projects/group-management.html', {
        "projects": Project.objects.all(),
        "project_form": project_form,
        "objective_formset": objective_formset,

    })


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            members_queryset = form.cleaned_data.get("members")
            for member in members_queryset.all():
                Membership.objects.create(user=member, project=project)
            return render(request, 'projects/includes/_project-card.html', {
                "project": project,
            })
        else:
            data = form.errors.as_json()
            return JsonResponse(data, safe=False, status=400)
    else:
        return HttpResponse(request.method)


def edit_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            print(">>>>>>>>>>>>>>>>>>", form.cleaned_data)
            project = form.save(commit=False)
            project.save()
            members_queryset = form.cleaned_data.get("members")
            # ProjectMembers.objects.filter(project=project).delete()
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", members_queryset.all().values_list('id', flat=True))
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", Membership.objects.filter(project=project))
            for id in Membership.objects.select_related().filter(project=project).values_list('user__id', flat=True):
                if id not in members_queryset.all().values_list('id', flat=True):
                    Membership.objects.filter(project=project, user__id=id).delete()

            for member in members_queryset.all():

                if not Membership.objects.filter(project=project, user=member).exists():
                    Membership.objects.create(user=member, project=project)

            return render(request, 'projects/includes/_project-card.html', {
                'project': project,
            })
        else:
            data = form.errors.as_json()
            return JsonResponse(data, safe=False, status=400)


def archive_project(request, project_id):
    instance = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        instance.active = False
        instance.save()
        message = "Projet archivé avec succès"
        return render(request, 'portal/message-modal.html', {'message': message})



def block_member(request, project_id, member):
    status = request.POST.get('member_status')
    print(">>>>>>>>>>>>>>>>>>>>>>>>", status)
    if status in ['True', 'False']:
        member = Membership.objects.filter(project__id=project_id, user__username=member)
        member.update(active=not eval(status))
        return JsonResponse({"status": 'ok'}, safe=False, status=200)
    else:
        return JsonResponse({"status": 'fail'}, safe=False, status=400)


def affect_user(request):
    return render(request, 'projects/users-affectation.html', {})


def configure_project(request, project_id, user):
    project = Project.objects.get(pk=project_id)

    objectives_formset = inlineformset_factory(Project, SecondaryObjective, form=SecondaryObjectiveForm,
                                                      extra=3, can_delete=False,)
    objectives_formset = objectives_formset(initial=SecondaryObjective.objects.all().values())
    project_form = ProjectForm(instance=project)
    resources = Publication.objects.filter(project=project, archived=False)
    members = Membership.objects.filter(project__id=project_id)
    members_ids = members.values_list("user_id", flat=True)
    return render(request, 'projects/project-configurations-modal.html', {
        "project_form": project_form,
        "objectives_formset": objectives_formset,
        "resources": resources,
        "members": members,
        "members_ids": members_ids,
        "project": project,
        "user": user,
    })
