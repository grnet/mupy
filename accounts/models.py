from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
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


def create_user_profile(sender, instance, created, **kwargs):
    if created and not kwargs.get('raw', False):
        UserProfile.objects.create(user=instance)
        to_emails = [admin[1] for admin in settings.ADMINS]
        send_mail(
            '[Mupy] new user',
            'New user created: %s. Give him some nodes to watch!' % (
                instance.username
            ),
            settings.DEFAULT_FROM_EMAIL,
            to_emails,
            fail_silently=False
        )

post_save.connect(create_user_profile, sender=User, dispatch_uid='create_UserProfile')
