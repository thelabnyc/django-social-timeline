from .models import Follow, Action
from django.contrib.contenttypes.models import ContentType


def get_content_type(obj):
    return ContentType.objects.get_for_model(obj)


class FollowMixin(object):
    def _get_follow(self, followee):
        try:
            follow = Follow.objects.get(
                follower_content_type=get_content_type(self),
                follower_object_id=self.id,
                followee_content_type=get_content_type(followee),
                followee_object_id=followee.id,
            )
            return follow
        except Follow.DoesNotExist:
            return None

    def follow(self, followee):
        follow = self._get_follow(followee)
        if follow is None:
            follow = Follow(follower=self, followee=followee)
            follow.save()
        return follow

    def unfollow(self, followee):
        follow = self._get_follow(followee)
        if follow is not None:
            follow.delete()

    def is_following(self, followee):
        follow_count = Follow.objects.filter(
            follower_content_type=get_content_type(self),
            follower_object_id=self.pk,
            followee_content_type=get_content_type(followee),
            followee_object_id=followee.pk,
        ).count()
        if follow_count > 0:
            return True
        return False

    def get_followers(self):
        return Follow.objects.filter(
            followee_content_type=get_content_type(self),
            followee_object_id=self.pk,
        )

    def get_followings(self, target_content_type=None):
        return Follow.objects.filter(
            follower_content_type=get_content_type(self),
            follower_object_id=self.pk,
        )

    def get_followers_count(self):
        return self.get_followers().count()

    def get_followings_count(self):
        return self.get_followings().count()

    def get_followings_ids(self):
        return self.get_followings().values_list(
            'followee_object_id', flat=True)

    def get_timeline(self, myself=False, verb=None, count=None, time=None):
        if myself is True:
            ids = [self.pk]
        else:
            ids = self.get_followings_ids()
        ct = get_content_type(self)
        actions = Action.get_timeline(verb=verb, time=time)
        actions = actions.filter(
            actor_object_id__in=ids,
            actor_content_type=ct,
        )
        if count is not None:
            actions = actions[:count]
        return actions

    def create_action(self, verb, target=None, timestamp=None):
        return Action.create_action(
            self, verb, target=target, timestamp=timestamp)
