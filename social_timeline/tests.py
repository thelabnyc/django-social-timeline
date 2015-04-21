from django.test import TestCase
from .mixin import FollowMixin
from .models import Action
from django.contrib.auth.models import User
import random
import string
import time


def get_random(N=10):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


class FollowUser(FollowMixin, User):
    class Meta:
        proxy = True


class FollowTestCase(TestCase):
    def setUp(self):
        self.user1 = FollowUser.objects.create_user('1')
        self.user2 = FollowUser.objects.create_user('2')
        self.user3 = FollowUser.objects.create_user('3')

    def test_follow(self):
        self.user1.follow(self.user2)
        self.assertTrue(self.user1.is_following(self.user2))
        self.user1.follow(self.user2)  # Should do nothing
        self.assertTrue(self.user1.is_following(self.user2))
        self.assertEquals(self.user1.get_followings_count(), 1)
        self.assertEquals(self.user2.get_followings_count(), 0)
        self.assertEquals(self.user1.get_followers_count(), 0)
        self.assertEquals(self.user2.get_followers_count(), 1)

    def test_multiple_follow(self):
        self.user1.follow(self.user2)
        self.user1.follow(self.user3)
        self.assertEquals(self.user1.get_followings_count(), 2)

    def test_action(self):
        Action.create_action(self.user1, 'joins')
        Action.create_action(self.user1, 'follows', self.user2)

    def test_timeline(self):
        self.user1.follow(self.user2)
        Action.create_action(self.user2, 'joins')
        Action.create_action(self.user2, 'insults', self.user1)
        Action.create_action(self.user3, 'ignores', self.user1)
        actions = self.user1.get_timeline()
        self.assertAlmostEquals(actions.count(), 2)

    def test_timeline_performance(self):
        friends = 100
        actions_per_friend = 100
        paginate_actions = 100
        for i in range(friends):
            user = FollowUser.objects.create_user(get_random())
            self.user1.follow(user)
            for j in range(actions_per_friend):
                Action.create_action(user, 'insults', self.user3)
        start = time.time()
        actions = self.user1.get_timeline(count=paginate_actions)
        for action in actions:
            x = action.actor
        run_time = time.time() - start
        self.assertLess(run_time, 1.0)
