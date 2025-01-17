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
    authentication_classes=[TokenAuthentication]
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

*TokenAuthentication
Basic-, Session-의 한계, Moblie Client에 적합함
authtoken 앱을 등록하고 migrate 시켜줘야 함 -> 왜? authtoken/models.py의 Token class에 유저별로 1:1 매칭되는 OneToOneField를 이용해 토큰을 발급할거니까용
1. username, password와 1:1 매칭되는 고유 key생성, 발급
2. 발급받은 token을 api요청에 담아 인증 처리
    *token 생성 방법 (보통 user객체가 생성될 때 자동으로 생성 x임 -> django.db.models.signals에 post_save를 사용하면 가능)
    1. rest_framework/authtoken/views.py의 ObtainAuthToken을 이용한 생성
    2. python 명령어를 통한 생성 (python manage.py drf_create_token <username>),(python manage.py drf_create_token -r <username>)


*permission 설정
1. settings.py에 'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.IsAuthenticated','[permission_class]'] 추가
2. view에 from rest_framework.permissions import [permission class] 하고 CBV에 permission_class = [permission class] 추가
3. fbv라면 @permission_classes([permission class]) 데코레이터 추가

*permission 종류
AllowAny: default 설정. 인증된 요청이든 비인증요청이든 전부 허용
IsAuthenticated : 인증된 요청에 대해서만 view 호출 허용
IsAdminUser : User.is_staff == True 일 때만 허용 <- django.contrib.auth.models import User 모델에 있는 속성임~
IsAuthenticatedOrReadOnly : 비인증요청은 읽기만 허용 (비인증요청은 안전한 http method만 허용 get,head,option 등)
"""