from rest_framework import routers

from post_app.views import ListPostView, DetailPostView

router = routers.SimpleRouter()

router.register(r'api/posts', ListPostView)
router.register(r'api/post', DetailPostView)

urlpatterns = router.urls
