from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from apps.watchlist import models
from apps.watchlist import serializers

# Create your tests here.


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser",
                                             password="test1234")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about="#1 OTT Service",
                                                           website="http://www.stream.com")

    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "American OTT",
            "website": "https://www.netflix.com"
        }

        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_detail(self):
        response = self.client.get(
            reverse('streamplatform-detail', args=[self.stream.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser",
                                             password="test1234")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about="#1 OTT Service",
                                                           website="http://www.stream.com")
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="test",
                                                         storyline="test", active=True)

    def test_watchlist_create(self):
        data = {
            "platform": self.stream.id,
            "title": "Test Movie",
            "storyline": "Test",
            "active": True
        }

        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_detail(self):
        response = self.client.get(
            reverse('movie-detail', args=[self.watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, 'test')


class ReviewTestCse(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser",
                                             password="test1234")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about="#1 OTT Service",
                                                           website="http://www.stream.com")
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="test",
                                                         storyline="test", active=True)
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream, title="test2",
                                                          storyline="test2", active=True)
        self.review = models.Review.objects.create(review_user=self.user,
                                                   rating=5,
                                                   comment="test description",
                                                   watchlist=self.watchlist2,
                                                   active=True)

    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "comment": "test-description",
            "watchlist": self.watchlist,
            "active": True
        }

        response = self.client.post(
            reverse('review-create', args=[self.watchlist.id]), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            reverse('review-create', args=[self.watchlist.id]), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(models.Review.objects.count(), 2)

    def test_review_create_unauth(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "test-description",
            "watchlist": self.watchlist,
            "active": True
        }

        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse('review-create', args=[self.watchlist.id]), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "test-description - Updated",
            "watchlist": self.watchlist2,
            "active": False
        }

        response = self.client.put(
            reverse('review-detail', args=[self.review.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(
            reverse('review-list', args=[self.watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_detail(self):
        response = self.client.get(
            reverse('review-detail', args=[self.review.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_user(self):
        response = self.client.get(
            '/watch/user-reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
