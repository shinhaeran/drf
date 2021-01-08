from django.shortcuts import render
from .serializer import UserSerializer
from .models import UserPost
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication

#Filtering , Search
"""
Filtering: Request 걸러보내기 -> ex) request: 특정 user의 특정 model list를 보여줘
Search: Response 걸러받기 -> ex) response : 특정 modeld의 특정 column을 대상으로 문자열 검색 진행

*내가 보낸 http request 참조하기*
내가 보낸 request : self.request
내가 보낸 request의 user : Self.request.user
내가 보낸 GET request : Self.request.GET (= self.request.query_param 가 사용 👆)
내가 보낸 POST request : Self.request.POST

서치 참고 : https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
"""
# Create your views here.
class UserPostViewSet(viewsets.ModelViewSet):
    authentication_classes=[BasicAuthentication,SessionAuthentication]
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
    
    def perform_create(self,serializer): #create Mixin 호출 메소드
        serializer.save(author=self.request.user)

    

"""
인증 : 서비스를 이용하는 데에 있어 내가 어느 정도의 권한이 있음을 요청하는(알려주는) 과정
허가 : 요청을 보낸 사용자에 대해 서비스를 어느정도 이용할 수 있는 지에 대한 권한

*인증 종류
BasicAuthentication : http 자체 기본인증에 기반한 인증방식 , ID+PW를 base64방식의 encoding ->완전 잘뚫린다
TokenAuthentication : 토큰헤더에서 사용자에게 유일한 key값 발급
SessionAuthentication : django default값 -> sessionMiddleware에서 로그인 될때마다 저장되는 session정보를 참조하여 인증
RemoteUserAuthentication : user정보가 다른 서비스에서 관리될 때 쓰이는 인증 방식

*httpie로 인증 POST 요청하기
http --form --auth 1:1 POST http://127.0.0.1:8000/userpost/ title="얍" body="b1"
"""