from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class Follow(models.Model):
    follower_content_type = models.ForeignKey(ContentType)
    follower_object_id = models.PositiveIntegerField()
    follower = GenericForeignKey('follower_content_type', 'follower_object_id')
    followee_content_type = models.ForeignKey(
        ContentType, related_name="followee_follow_set")
    followee_object_id = models.PositiveIntegerField()
    followee = GenericForeignKey('followee_content_type', 'followee_object_id')
    is_mutual = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            (
                'follower_content_type',
                'follower_object_id',
                'followee_content_type',
                'followee_object_id',
            ),
        )


class Action(models.Model):
    actor_content_type = models.ForeignKey(ContentType)
    actor_object_id = models.PositiveIntegerField()
    actor = GenericForeignKey('actor_content_type', 'actor_object_id')
    verb = models.CharField(max_length=255)
    target_content_type = models.ForeignKey(
        ContentType, blank=True, null=True, related_name="target_action_set")
    target_object_id = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def _get_link(self, obj):
        if obj is None:
            return
        if hasattr(obj, 'get_absolute_url'):
            return obj.get_absolute_url()

    def actor_link(self):
        return self._get_link(self.actor)

    def target_link(self):
        return self._get_link(self.target)

    @staticmethod
    def create_action(actor, verb, target=None, timestamp=None):
        action = Action(actor=actor, verb=verb)
        if target is not None:
            action.target = target
        if timestamp is not None:
            action.timestamp = timestamp
        action.save()
        return action

    @staticmethod
    def get_timeline(verb=None, count=None, time=None):
        actions = Action.objects.all()
        if verb:
            actions = actions.filter(verb=verb)
        if time:
            actions = actions.filter(timestamp__lte=time)
        if count is not None:
            actions = actions[:count]
        return actions
