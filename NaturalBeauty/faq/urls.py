from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from .views import HomeView, MyView, CategoryViewSet, FaqViewSet, RegisterView
from .views import CategoryView
from .views import FaqUnlockedView
from .views import StartFaqView
from .views import UpdateFaqView

router = routers.DefaultRouter()
router.register('category', CategoryViewSet)
router.register('faq', FaqViewSet)

urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home"
    ),
    path(
        'register',
        RegisterView.as_view(),
        name='register'
    ),
    path(
        'category/<int:category_id>',
        CategoryView.as_view(),
        name='category'
    ),
    path(
        'unlock',
        login_required(FaqUnlockedView.as_view()),
        name='unlock'
    ),
    path(
        'start',
        StartFaqView.as_view(),
        name='start'
    ),
    path(
        'update/<int:faq_id>',
        login_required(UpdateFaqView.as_view()),
        name='update'
    ),
    path(
        'my',
        login_required(MyView.as_view()),
        name='my'
    ),
    path(
        'api/',
        include(router.urls)
    ),
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    )
]

# EOF
