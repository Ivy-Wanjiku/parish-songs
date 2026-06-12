from django.http import FileResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Q

from .models import Song
from .serializers import SongSerializer


class IsAdminUser(IsAuthenticated):
    def has_permission(self, request, view) -> bool:
        return (
            super().has_permission(request, view)
            and getattr(request.user, 'role', None) in ('admin', 'superadmin')
        )


class SongListView(generics.ListCreateAPIView):
    serializer_class = SongSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        qs = Song.objects.all()
        params = self.request.query_params

        category = params.get('category')
        misa_id = params.get('misa_id')
        language = params.get('language')
        search = params.get('search', '').strip()

        if category:
            qs = qs.filter(category=category)
        if misa_id:
            qs = qs.filter(misa_id=misa_id)
        if language:
            qs = qs.filter(language=language)
        if search:
            qs = qs.filter(
                Q(title__icontains=search) | Q(lyrics__icontains=search)
            )

        return qs


class SongDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]


class ScoreDownloadView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk: int):
        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response({'error': 'Song not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not song.has_score or not song.score_file:
            return Response(
                {'error': 'No score available for this song.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            file_handle = song.score_file.open('rb')
        except (FileNotFoundError, OSError):
            return Response(
                {'error': 'Score file not found on server.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        safe_title = song.title.replace('/', '_').replace('..', '_')
        response = FileResponse(file_handle, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{safe_title}.pdf"'
        return response
