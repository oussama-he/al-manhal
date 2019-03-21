import math

from django.db import models
from taggit.managers import TaggableManager
from accounts.models import User
from projects.models import Project

from utils.utils import upload_to


class Publication(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    content = models.TextField(blank=True, verbose_name="Annotation")
    source = models.FileField(upload_to=upload_to, blank=True, verbose_name="La source")
    source_url = models.URLField(blank=True, verbose_name="La source")
    tags = TaggableManager()
    user = models.ForeignKey(User, default=1)
    # todo: make project field required
    project = models.ForeignKey(Project, verbose_name="Projet")
    rating = models.ManyToManyField(User, through='Rating', related_name='rating')
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=300, blank=True, verbose_name="Sujet")
    contributor = models.CharField(max_length=300, blank=True, verbose_name="Contributeur")
    coverage = models.CharField(max_length=300, blank=True, verbose_name="couverture")
    creator = models.CharField(max_length=300, blank=True, verbose_name="Createur")
    date = models.DateField(blank=True, null=True)
    description = models.TextField(max_length=1500, blank=True)
    format = models.CharField(max_length=100, blank=True)
    identifier = models.CharField(max_length=100, blank=True, verbose_name="Identifiant")
    publisher = models.CharField(max_length=300, blank=True, verbose_name="Editeur")
    relation = models.CharField(max_length=300, blank=True)
    rights = models.TextField(max_length=1500, blank=True, verbose_name="Droits")
    type = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=100, blank=True, verbose_name="Langue")

    def __str__(self):
        return "{}".format(self.title)

    def get_score(self):
        score = 0
        rates = Rating.objects.filter(publication=self)
        if rates.count():
            for rate in rates:
                score += rate.rating
                print(">>>>>>>>>>>>>>>>>>>>>>>>>", round(score / rates.count(), 2))
            return round(score / rates.count(), 2)
        else:
            return score

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.user.username, self.publication.title)

    class Meta:
        ordering = ['-published_date']


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='rate')
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, blank=True, related_name='rated')
    rating = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "{}-{}-{}".format(self.publication.title, self.user.username, self.rating)

    # class Meta:
    #     unique_together = ("user", "publication")
    #

