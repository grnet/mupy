from django.db import models
from django.contrib.auth.models import User
from mupy.muparse.models import *


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    nodegroups = models.ManyToManyField(NodeGroup, blank=True, null=True)
    
    def get_nodegroups(self):
        ret = ''
        ngs = self.nodegroups.all()
        for ng in ngs:
            ret = "%s, %s" %(ng, ret)
        if ret:
            ngroups = ret.rstrip(', ')
            return ngroups
        else:
            return None
    
    def __unicode__(self):
        return "%s:%s" %(self.user.username, self.get_nodegroups())
