from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from muparse.models import Node


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    nodes = models.ManyToManyField(Node, blank=True, null=True)

    def get_nodes(self):
        ret = ''
        ngs = self.nodes.all()
        for ng in ngs:
            ret = "%s, %s" %(ng, ret)
        if ret:
            nodes = ret.rstrip(', ')
            return nodes
        else:
            return None

    def save(self, *args, **kwargs):
        cache.delete('user_%s_tree' % (self.user.pk))
        cache.delete('user_%s_tree_cat' % (self.user.pk))
        super(UserProfile, self).save(*args, **kwargs)


    def __unicode__(self):
        return "%s:%s" %(self.user.username, self.get_nodes())
