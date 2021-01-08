"""firstrest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import post.urls,userpost.urls
from rest_framework import urls
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/',include('post.urls')),
    path('userpost/',include('userpost.urls')),
    path('api-auth/',include('rest_framework.urls')), #헤드에 로그인로그아웃 가능한 버튼이 생긴다! 대신 BasicAuthentication이 아니고 TokenAuthentication으로 해야 된다
    path('api-token-auth/',obtain_auth_token), #발급한 토큰을 획득
]

"""
*터미널에서 토큰 발급 받고
python manage.py drf_create_token 1
    Generated token b95c0a7eb1a9fd899099515659e763899b94d9c6 for user 1

*httpie로 발급받은 토큰 얻기(확인)
http  POST http://127.0.0.1:8000/api-token-auth/ username="1" password="1"
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 52
Content-Type: application/json
Date: Fri, 08 Jan 2021 16:43:59 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "token": "b95c0a7eb1a9fd899099515659e763899b94d9c6"
}

*httpie로 얻은 토큰으로 post요청하기
http  POST http://127.0.0.1:8000/userpost/ "Authorization: Token b95c0a7eb1a9fd899099515659e763899b94d9c6" title="인증" body="인증인증"
"""
