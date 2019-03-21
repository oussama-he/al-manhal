import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from taggit.models import Tag

from accounts.forms import SignUpForm, SignInForm
from django.contrib.auth import login
from portal.models import Publication, Rating
from projects.models import Project
from .forms import ResourceForm, CommentForm, RatingForm, TagsForm, FilterProjectForm


def home(request):
    sign_in_form = SignInForm()
    sign_up_form = SignUpForm()

    return render(request, 'home.html', {
        'sign_in_form': sign_in_form,
        'sign_up_form': sign_up_form,
    })


@login_required
def create_resource(request, source):
    if request.method == 'POST':
        form = ResourceForm(request.POST, files=request.FILES or None, user=request.user)
        if form.is_valid():
            print(">>>>>>>>>>>>>>>>>>>>>>>>> from form is valid")
            resource = form.save(commit=False)
            resource.user = request.user
            resource.save()
            form.save_m2m()
            if source == "profile":
                return render(request, "accounts/includes/_resource-card.html", {"resource": resource})
            elif source == 'extension':
                return JsonResponse({'status': 'ok'}, safe=False, status=200)
            else:
                return render(request, 'portal/includes/_pub-card.html', {
                                    'publication': resource,
                                    'comment_form': CommentForm()
                            })
        else:
            data = form.errors.as_json()
            return JsonResponse(data, safe=False, status=400)


@login_required
def edit_resource(request, pub_id, source):
    instance = Publication.objects.get(id=pub_id)
    if request.method == 'POST':
        form = ResourceForm(request.POST, files=request.FILES or None, instance=instance, user=request.user)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.user = request.user
            resource.save()
            form.save_m2m()

            if source == 'profile':
                return render(request, 'accounts/includes/_resource-card.html', {
                    'resource': resource,
                })
            else:
                return render(request, 'portal/includes/_pub-card.html', {
                    'publication': resource,
                    'comment_form': CommentForm()
                })
        else:
            data = form.errors.as_json()
            print("form is not valid", data)
            return JsonResponse(data, safe=False, status=400)


def rate_resource(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        # todo revise this function
        if form.is_valid():
            publication_id = request.POST.get('publication-id')
            publication = Publication.objects.get(pk=publication_id)
            if Rating.objects.filter(user=request.user, publication=publication).count() == 0:
                rate = form.save(commit=False)
                rate.user = request.user
                rate.publication = publication
                rate.rating = int(request.POST.get("rating"))
                rate.save()
            else:
                user_rating = Rating.objects.get(user=request.user, publication=publication)
                user_rating.user = request.user
                user_rating.publication = publication
                user_rating.rating = int(request.POST.get("rating"))
                user_rating.save()
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>", publication.get_score())
            response = '{"publication_score": %.1f}' % publication.get_score()
            return HttpResponse(json.dumps(response), content_type="application/json")
            # else:
            #     return JsonResponse({"error": "you can't rate twice"}, safe=False, status=400)
            # return render(request, 'portal/includes/_pub-comment.html', {'comment': comment})
        else:
            data = form.errors.as_json()
            print("form is not valid", data)
            return JsonResponse(data, safe=False, status=400)


def get_rating(request, pub_id):
    publication = Publication.objects.get(pk=pub_id)
    response = dict()
    response["rating"] = float(publication.get_score())
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def create_comment(request, pub_id):
    publication = Publication.objects.get(pk=pub_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.publication = publication
            comment.save()
            # return HttpResponse(json.dumps("{'status': 'ok'}"), content_type="application/json")
            return render(request, 'portal/includes/_pub-comment.html', {'comment': comment})
        else:
            data = form.errors.as_json()
            print("form is not valid", data)
            return JsonResponse(data, safe=False, status=400)


@login_required
@xframe_options_exempt
def display_publications(request):
    projects = Project.objects.filter(Q(created_by=request.user) | Q(members__id__in=[request.user.id]), active=True).distinct()
    publications = Publication.objects.filter(project__in=projects, archived=False)
    tags = Tag.objects.filter(publication__in=publications).distinct()
    print(">>>>>>>>>>>>>>>>>>>>>>>>>", tags)
    # projects = Project.objects.filter(id__in=publications.values('project_id')).distinct()
    if request.method == 'GET':
        tags_form = TagsForm(request.GET, tags=tags)
        filter_project_form = FilterProjectForm(request.GET, projects=projects)
        if tags_form.is_valid():
            # do something
            tags_id = request.GET.getlist('filter_tags')
            projects_id = request.GET.getlist('filter_projects')
            if len(tags_id) > 0 and len(projects_id) > 0:
                tags_id = [int(i) for i in tags_id]
                projects_id = [int(i) for i in projects_id]
                publications = publications.filter(project__id__in=projects_id, tags__id__in=tags_id, archived=False,).distinct()
            elif len(tags_id) > 0:
                tags_id = [int(i) for i in tags_id]
                publications = publications.filter(tags__id__in=tags_id, archived=False,).distinct()
            elif len(projects_id) > 0:
                projects_id = [int(i) for i in projects_id]
                publications = publications.filter(project__id__in=projects_id, archived=False, ).distinct()
            return render(request, 'portal/publications.html', {
                'publication_form': ResourceForm(user=request.user),
                'comment_form': CommentForm(),
                'publications': publications,
                'tags_form': tags_form,
                'filter_project_form': filter_project_form,
            })
        else:
            return render(request, 'portal/publications.html', {
                'publication_form': ResourceForm(user=request.user),
                'comment_form': CommentForm(),
                'publications': publications,
                'tags_form': tags_form,
                'filter_project_form': filter_project_form,
            })

"""
@login_required
def delete_publication(request, pub_id):
    instance = get_object_or_404(Publication, pk=pub_id)
    if request.method == 'POST':
        instance.delete()
        # return JsonResponse("Publication Supprimer avec success")
        message = "Ressource supprimée avec succès"
        return render(request, 'portal/message-modal.html', {'message': message})
"""

@login_required
def archive_publication(request, pub_id):
    instance = get_object_or_404(Publication, pk=pub_id)
    if request.method == 'POST':
        instance.archived = True
        instance.save()
        # return JsonResponse("Publication Supprimer avec success")
        message = "Ressource archivée avec succès"
        return render(request, 'portal/message-modal.html', {'message': message})


@login_required
def get_publication_meta_data(request, pub_id, user):
    resource = Publication.objects.get(pk=pub_id)
    form = ResourceForm(instance=resource, user=request.user)
    # form = PublicationForm({'title': 'pub 1'})
    # return HttpResponse('<h1>Success</h1>')
    return render(request, 'portal/_meta-data-modal.html', {
        'form': form,
        'resource': resource,
        'user': user
    })


@xframe_options_exempt
def extension_view(request):
    if request.user.is_authenticated():
        form = ResourceForm(user=request.user)
        return render(request, 'portal/ext_main.html', {"form": form})
