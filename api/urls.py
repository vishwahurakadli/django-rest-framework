from home.views import index, person, login, PersonAPI, PeopleViewSet, RegisterAPI, LoginAPI
from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'people', PeopleViewSet, basename='people')
urlpatterns = router.urls

urlpatterns =[
    path('', include(router.urls)),
    path('index/', index, name='index'),
    path('person/',person, name='person'),
    # path('login/',login, name='login'),
    path('persons/', PersonAPI.as_view(), name='classView'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(),name='login_class')
]