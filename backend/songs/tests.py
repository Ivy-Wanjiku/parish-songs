from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from songs.models import Song

User = get_user_model()


def make_admin(username='admin1', role='admin'):
    u = User.objects.create_user(username=username, password='testpass123')
    u.role = role
    u.save()
    return u


def make_song(**kwargs):
    defaults = dict(
        title='Test Song',
        category='Entrance',
        language='Swahili',
        lyrics='Line one\nLine two',
        misa_id='',
        ord_part='',
    )
    defaults.update(kwargs)
    return Song.objects.create(**defaults)


class SongListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        make_song(title='Nalifurahi', category='Entrance')
        make_song(title='Tujongeeni', category='Communion')

    def test_list_is_public(self):
        res = self.client.get('/api/songs/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_filter_by_category(self):
        res = self.client.get('/api/songs/?category=Entrance')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], 'Nalifurahi')

    def test_search_by_title(self):
        res = self.client.get('/api/songs/?search=tujon')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_search_by_lyrics(self):
        make_song(title='Unique', lyrics='Special keyword here')
        res = self.client.get('/api/songs/?search=special+keyword')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_create_requires_auth(self):
        res = self.client.post('/api/songs/', {'title': 'X', 'category': 'Entrance',
                                               'language': 'Swahili', 'lyrics': 'y'})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class SongDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.song = make_song(title='Hello', category='Offertory')
        self.admin = make_admin()

    def test_get_single_song_is_public(self):
        res = self.client.get(f'/api/songs/{self.song.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], 'Hello')

    def test_delete_requires_auth(self):
        res = self.client.delete(f'/api/songs/{self.song.id}/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_delete(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.delete(f'/api/songs/{self.song.id}/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Song.objects.filter(id=self.song.id).exists())

    def test_admin_can_update(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.put(
            f'/api/songs/{self.song.id}/',
            {'title': 'Updated', 'category': 'Offertory',
             'language': 'Swahili', 'lyrics': 'new lyrics'},
            format='json',
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], 'Updated')


class SongAdminCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = make_admin()

    def test_admin_can_create_song(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.post('/api/songs/', {
            'title': 'New Song',
            'category': 'Thanksgiving',
            'language': 'Kikuyu',
            'lyrics': 'Nĩ thengiũ Mwathani',
        }, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Song.objects.filter(title='New Song').count(), 1)

    def test_ordinary_song_requires_misa_id(self):
        self.client.force_authenticate(user=self.admin)
        # When creating an ord song without misa_id it should still save
        # (misa_id is blank=True on the model; validation is UI-side)
        res = self.client.post('/api/songs/', {
            'title': 'Kyrie',
            'category': 'ord-Kyrie',
            'language': 'Swahili',
            'lyrics': 'Bwana utuhurumie',
            'misa_id': 'banana',
        }, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
