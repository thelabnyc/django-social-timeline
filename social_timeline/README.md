## API

There is no out of the box api - but it's easy to enable and modify it if you 
are using Django Rest Framework 3.0+. I'll assume you already know the basics of DRF.

Register the ActionViewSet or use it as a base class for your own.

```
from rest_framework import routers
from social_timeline.api_views import ActionViewSet 

router = routers.DefaultRouter()
router.register(r'actions', ActionViewSet)

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    ...
```
