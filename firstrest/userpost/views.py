from django.shortcuts import render
from .serializer import UserSerializer
from .models import UserPost
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

#Filtering , Search
"""
Filtering: Request 걸러보내기 -> ex) request: 특정 user의 특정 model list를 보여줘
Search: Response 걸러받기 -> ex) response : 특정 modeld의 특정 column을 대상으로 문자열 검색 진행

*내가 보낸 http request 참조하기*
내가 보낸 request : self.request
내가 보낸 request의 user : Self.request.user
내가 보낸 GET request : Self.request.GET (= self.request.query_param 가 사용 👆)
내가 보낸 POST request : Self.request.POST

필터링 참고 : https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
"""
# Create your views here.
class UserPostViewSet(viewsets.ModelViewSet):
    queryset = UserPost.objects.all()
    serializer_class = UserSerializer
    # filter_backends = [SearchFilter] #어떤걸 기반으로 검색할거야
    filter_backends = [DjangoFilterBackend]
    # search_fields = ('title','author')#어떤 컬럼을 기반으로 검색할거야? -> 무조건 튜플로
    filterset_fields = ['title', 'author']
    def get_queryset(self): #filtering
        qs = super().get_queryset()
        # print(self.request.user.is_authenticated) #True / False
        if self.request.user.is_authenticated: #self.request.user.id
            print(self.request.user)
            qs = qs.filter(author =self.request.user) #or .exclude 그리고 id 접근 : author__id
        else:
            qs = qs.none() # <QuerySet []>
            print(qs)
        
        return qs