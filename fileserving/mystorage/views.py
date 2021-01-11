from django.shortcuts import render
from rest_framework import viewsets
from .models import Essay,Album,File
from .serializers import EssaySerializer,FileSerializer,AlbumSerializer
from rest_framework.filters import SearchFilter
# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset=Essay.objects.all()
    serializer_class = EssaySerializer
    filter_backends = [SearchFilter]
    search_fields = ('title','body')

    def perform_create(self,serializers):
        serializers.save(author=self.request.user)
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            qs=qs.filter(author=self.request.user)
        else:
            qs.none()
        return qs

class ImgViewSet(viewsets.ModelViewSet):
    queryset=Album.objects.all()
    serializer_class = AlbumSerializer

from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
from rest_framework import status
class FileViewSet(viewsets.ModelViewSet):
    queryset=File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,FormParser) # 다양한 미디어 타입으로 request를 수락하는 방법들 -> 인코딩방식이 다 다르기 때문에 필요하다고 한다. 근데 나는 없어도 잘 되는디?

    def post(self,request,*args,**kwargs): #post 메소드 오버라이딩
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)



    