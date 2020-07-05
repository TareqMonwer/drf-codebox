from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.permissions import IsOwnerOrReadOnly


class SnippetViewSet(viewsets.ModelViewSet):
	"""
	This viewset automatically provides 'list', 'create', 'retrieve',
	'update' and 'destroy' actions.
	Additionally we provide an extra 'hightlight' action.
	"""
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly,
						  IsOwnerOrReadOnly]

	@action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
	def highlight(self, *args, **kwargs):
		snippet = self.get_object()
		return Response(snippet.highlighted)

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)



@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'snippets': reverse('snippet-list', request=request, format=format)
	})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	This viewset automatically provides 'list' and 'detail' actions.
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
