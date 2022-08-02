import hashlib
import os
from django.db import models
from fir_plugins.models import ManyLinkableModel, OneLinkableModel


class ArtifactBlacklistItem(models.Model):
    type = models.CharField(max_length=20)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.value


class Artifact(ManyLinkableModel):
    type = models.CharField(max_length=20)
    value = models.TextField()

    def __str__(self):
        display = self.value
        if self.relations.count() > 1:
            display += f" ({self.relations.count()})"
        return display


def upload_path(instance, filename):
    return f"{instance.content_type.model}_{instance.object_id}/{filename}"


class File(OneLinkableModel):

    hashes = models.ManyToManyField('fir_artifacts.Artifact', blank=True)
    description = models.CharField(max_length=256)
    file = models.FileField(upload_to=upload_path)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return unicode(self.file.name)

    def getfilename(self):
        return os.path.basename(self.file.name)

    def get_hashes(self):
        hashes = {k: None for k in ['md5', 'sha1', 'sha256']}
        content = self.file.read()
        for algo in hashes:
            m = hashlib.new(algo)
            m.update(content)
            hashes[algo] = m.hexdigest()
        return hashes
