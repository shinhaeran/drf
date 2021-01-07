
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register('',views.PostViewSet)
urlpatterns = [
    path('',include(router.urls)),
    # path('post/',views.PostList.as_view()),
    # path('post/<int:pk>/',views.PostDetail.as_view()),
]
"""
as_view({'[http_method]':'[처리할 함수 이름]'})이렇게 매핑할 수 있다~
mypath=PostViewSet.as_view({
    'get':'retrive',
    'put':'update',
    'patch':'partial_update',
    delete:'destroy'
})

-> mypath변수를 path('',mypath)로 넣으면 url을 묶어 하나의 viewset에 넣기 가능
->매핑관계 만드는게 중복되고 좀 귀찮을 수 있다 -> 관례적인 매핑을 자동으로 해주는게 router!(defaultrouter)
-> router의 register(prefix,viewset)
"""

