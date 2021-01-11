from .models import Essay,Album,File
from rest_framework import serializers
#source : field를 채우는데 사용할 속성의 이름. 중첩된 표현을 작성하거나 출력 표현을 결정하기 위해 전체 오브젝트에 액세스해야하는 필드에 유용합니다.

class EssaySerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Essay
        fields = ('pk','title','body','author_name')

class AlbumSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    image = serializers.ImageField(use_url=True) #이미지 업로드 하고 결과값의 확인작업을 url로 하겠다!
    class Meta:
        model = Album
        fields = ('pk','image','desc','author_name')

class FileSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    myfile = serializers.FileField(use_url=True)
    class Meta:
        model = File
        fields = ('pk','myfile','desc','author')