from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from lib import constants as const
from lib import errormessages as errorMessage
from post.serializers.postresponseserializer import PostResponseSerializer
from post.serializers.postsaveserializer import PostSaveSerializer
from post.models import Post

class PostListView(APIView):
	def get(self, request, format=None):
		try:
			queryset = Post.objects.all()
			serializer = PostResponseSerializer(queryset, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		except:
			return Response(
				{const.ERROR_PROPERTY : errorMessage.INTERNAL_SERVER_ERROR},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)

	def post(self, request, format=None):
		try:
			serializer = PostSaveSerializer(data=request.data)
			if serializer.is_valid():
				post = serializer.save()
				serializer = PostResponseSerializer(post)
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response(
					serializer.errors, status=status.HTTP_400_BAD_REQUEST
				)
		except:
			return Response(
				{const.ERROR_PROPERTY : errorMessage.INTERNAL_SERVER_ERROR},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)