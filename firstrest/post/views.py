from django.shortcuts import render
from .models import Post
from .serializer import PostSerializer
from rest_framework import status


#APIView -> 다른 모델에게도 같은 기능 적용하기에는 비효율적 -> viewset처럼 queryset, serializer_class만 정의해서 동작 x -> "detail": "Method \"GET\" not allowed."
from django.http import Http404,HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

# class PostList(APIView):
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts,many=True) #다수의 데이터 queryset형태를 selialize화 하고자 할 때 many=True사용-> 여러개의 객체니까 꼭 필수
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = PostSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.error, status = status.HTTP_400_BAD_REQUEST)
    
# class PostDetail(APIView):
#     def get_object(self,pk): #get_object_404를 구현하는 helper fucntion
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise Http404
#     def get(self,request,pk,format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#     def put(self,request,pk,format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request,pk,format=None):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#minxin
from rest_framework import generics,mixins

# class PostList(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
    

# class PostDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)
#     def delete(self,request,*args,**kwargs):
#         return self.destroy(*args,**kwargs)
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)

# generic view
from rest_framework import generics
#listcreateview -> list + create ; get, post 메소드 있
# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#viewset
"""
ReadOnlyViewSet : provides default 'list()' and 'retrieve' actions
ModelViewSet : provides default 'create' 'retrieve' 'update' 'patial_update' 'destroy' 'list' actions
action 데코레이터 : 밑에 crud 외 다른 로직들 -> custom api의 default method는 get방식. 임의로 action의 format인자로 지정 가능
"""
from rest_framework import viewsets,renderers
from rest_framework.decorators import action
# class PostViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #action(method=['post']) : 첫번째 인자 method를 post로 바꿀 때 
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs): #detail 페이지에서 [Extra Actions] 버튼에 동작 가능
        return HttpResponse("얍")
