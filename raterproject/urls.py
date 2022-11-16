from rest_framework import routers
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from raterapi.views import register_user, login_user
from raterapi.views import GameView, ReviewView, CategoryView, RatingView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', GameView, 'game')
router.register(r'reviews', ReviewView, 'review')
router.register(r'ratings', RatingView, 'rating')
router.register(r'categories', CategoryView, 'category')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
