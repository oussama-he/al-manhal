from django.db import models

from accounts.models import User


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=5000)
    objective = models.TextField(max_length=5000)
    duration = models.CharField(max_length=300)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    # members = models.ManyToManyField(User, through='Member', related_name='members')
    members = models.ManyToManyField(User, through='Membership', related_name='member')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-pk"]


class SecondaryObjective(models.Model):
    objective = models.CharField(max_length=500, blank=True)
    project = models.ForeignKey(Project)

    def __str__(self):
        return self.project.title


class Membership(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    project = models.ForeignKey(Project, blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{}-{}".format(self.user.username, self.project.title)

    @property
    def resources_count(self):
        resources = self.user.publication_set.all()
        count = 0
        for ressource in resources:
            if not ressource.archived:
                count += 1
        return count

"""
class InventoryTag(models.Model):
    class Meta:
        unique_together = ('key', 'value')

    key   = models.CharField(max_length=240, db_index=True)
    value = models.CharField(max_length=240, db_index=True)

class InventoryItem(models.Model):
    instance_id = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(InventoryTag, through='InventoryItemTag', through_fields=('item', 'tag'))

    def as_json(self):
        return serializers.serialize('json', [self])[0]

class InventoryItemTag(models.Model):
    class Meta:
        unique_together = ('item', 'tag')

    item = models.ForeignKey(InventoryItem, db_index=True, related_name='invitem')
    tag  = models.ForeignKey(InventoryTag, db_index=True, related_name='invtag')

    created_at = models.DateTimeField(auto_now_add=True)
 """