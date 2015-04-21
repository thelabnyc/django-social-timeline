# django-social-timeline

Social networking for django. Following system and timeline of events.
Heavily inspired by [django-sequere](https://github.com/thoas/django-sequere)
The main difference between the projects is that sequeue uses redis while social-timeline uses a database backend.
This allows the models to be easily queried but may not have the level of performance a redis backend has.
Check out the performance unit tests and consider your own needs.

Status: In development, not suitable for production use.

## Following

The concept of one entity following another. We use generic foreign keys to provide high flexibilty here. 
For example a user would follow another user. 
We can query who is following a user, or get the list of people a user is following.

## Actions (timeline)

Defined as a actor, verb, and target. Actor and target are both generic foreign keys. Target is optional.
Examples:

- Jane (actor) joins (verb)
- Joe (actor) comments (verb) on the blog post (our target could be the comment object or the blog post)

social_timeline provides some mixins to make it easy to do common tasks like getting a list of all actions taken by people a user is following.

# Installation and usage

Tested on django 1.7, 1.8. Python 3.4.

1. Add `social_timeline` to `INSTALLED_APPS`
2. Run migrations `./manage.py migrate`
3. Add FollowMixin to models you with to be capable of following or being followed.
    ```
    from social_timeline.mixin import FollowMixin

    class Profile(FollowMixin, models.Model):
        user = models.OneToOneField('auth.User')
    ```
4. Review [mixins.py](/social_Timeline/mixins.py) for all actions. Examples

```
user1.follow(user)
followering = user1.get_followings()
user1.get_timeline()
```

## API (optional)

A [starter api](/social_timeline/api_views.py) is included if you are using django-rest-framework. 
You may ignore it or extend it for more catered use.

# Hacking

First install docker and docker-compose. You don't need these but it makes it easier.

## Play around

1. run `docker-compose up`
2. run `docker-compose run --rm web ./manage.py migrate`
3. run `docker-compose run --rm web ./manage.py createsuperuser`

## Run tests

run `docker-compose run --rm web ./manage.py test`
