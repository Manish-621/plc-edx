# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from organizations.models import Organization
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserBatch(models.Model):
    class Meta(object):
        db_table = "usermanagement_userbatches"
        verbose_name = 'User Batches'
    
    organization = models.ForeignKey(Organization,null=False,related_name="userbatch_organization",on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=100)
    batch_description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=1)
    created_date = models.DateTimeField(null=True, default=timezone.now)
    last_modified_date = models.DateTimeField(null=True, default=timezone.now)

    def __unicode__(self):
        """Represent ourselves with the course key."""
        return unicode(self.organization.name +' | '+self.batch_name)

class UserBatchMapping(models.Model):
    class Meta(object):
        db_table = "usermanagement_userbatchmapping"
        verbose_name = 'User Batch Mapping'

    user = models.ForeignKey(User,null=False,related_name="userbatchmapping_user",on_delete=models.CASCADE)
    user_batch = models.ForeignKey(UserBatch,null=False,related_name="userbatchmapping_userbatch",on_delete=models.CASCADE)

    @classmethod
    def getLogoByUser(cls, user):
        user_batches = cls.objects.filter(user=user)
        if user_batches.exists():
            batch = user_batches.first().user_batch
            if batch.organization.logo and len(batch.organization.logo.url) > 1 :
                return batch.organization.logo.url
        return None