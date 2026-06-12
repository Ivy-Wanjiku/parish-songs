from rest_framework import serializers
from .models import Song


class SongSerializer(serializers.ModelSerializer):
    score_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Song
        fields = [
            'id', 'title', 'category', 'language', 'key_signature',
            'lyrics', 'misa_id', 'ord_part', 'has_score', 'score_file',
            'score_url', 'uploaded_by', 'uploaded_by_name',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'has_score', 'score_url',
            'uploaded_by', 'uploaded_by_name',
            'created_at', 'updated_at',
        ]
        extra_kwargs = {
            'score_file': {'write_only': True, 'required': False},
        }

    def get_score_url(self, obj: Song) -> str | None:
        if obj.has_score and obj.score_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(f'/api/songs/{obj.id}/score/')
        return None

    def create(self, validated_data: dict) -> Song:
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['uploaded_by'] = request.user
            full_name = (
                f"{request.user.first_name} {request.user.last_name}".strip()
                or request.user.username
            )
            validated_data['uploaded_by_name'] = full_name
        if validated_data.get('score_file'):
            validated_data['has_score'] = True
        return super().create(validated_data)

    def update(self, instance: Song, validated_data: dict) -> Song:
        if validated_data.get('score_file'):
            validated_data['has_score'] = True
        return super().update(instance, validated_data)
