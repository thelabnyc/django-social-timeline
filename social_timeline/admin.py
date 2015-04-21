from django.contrib import admin
from .models import Action, Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followee')
    related_lookup_fields = {
        'generic': [
            ['follower_content_type', 'follower_object_id'],
            ['followee_content_type', 'followee_object_id'],
        ],
    }


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('actor', 'verb', 'target', 'timestamp')
    list_filter = ('actor_content_type', 'verb', 'timestamp',
                   'target_content_type')
    related_lookup_fields = {
        'generic': [
            ['actor_content_type', 'actor_object_id'],
            ['target_content_type', 'target_object_id'],
        ],
    }
