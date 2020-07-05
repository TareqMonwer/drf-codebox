from rest_framework import serializers
from django.contrib.auth.models import User
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')
	highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight',
													 format='html')
	class Meta:
		model = Snippet
		fields = ['url', 'id', 'highlight', 
				  'title', 'owner', 'code', 'lineos', 'language', 'style']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail',
    											 read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']




# Without ModelSerializer
# class SnippetSerializer(serializers.Serializer):
# 	id = serializers.IntegerField(read_only=True)
# 	title = serializers.CharField(required=False, 
# 			allow_blank=True, max_length=100)
# 	code = serializers.CharField(style={'base_template': 'textarea.html'})
# 	lineos = serializers.BooleanField(required=False)
# 	language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
# 	style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

# 	def create(self, validated_data):
# 		"""
# 		Create and return a new `Snippet` instance, given the validate data.
# 		"""
# 		return Snippet.objects.create(**validated_data)

# 	def update(self, instance, validated_data):
# 		"""
# 		Update and return existing `Snippet` instance, given the validate data.
# 		"""
# 		instance.title = validated_data.get('title', instance.title)
# 		instance.code = validated_data.get('code', instance.code)
# 		instance.lineos = validated_data.get('lineos', instance.lineos)
# 		instance.language = validated_data.get('language', instance.language)
# 		instance.style = validated_data.get('style', instance.style)
# 		instance.save()
# 		return instance