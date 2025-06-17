from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Project, Proposal, Profile, Message, Review

class AuthTest(APITestCase):
    def test_register_and_login(self):
        # Register
        url = reverse('register')
        data = {
            'username': 'freelancer1',
            'password': 'testpass123',
            'email': 'f1@example.com',
            'is_freelancer': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Login
        url = reverse('token_obtain_pair')
        data = {'username': 'freelancer1', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class ProposalTest(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(username='client', password='pass', is_client=True)
        self.freelancer = User.objects.create_user(username='freelancer', password='pass', is_freelancer=True)
        self.project = Project.objects.create(
            client=self.client_user,
            title='Test Project',
            description='desc',
            budget=100,
            deadline='2025-12-31'
        )

    def test_freelancer_can_create_proposal(self):
        self.client.force_authenticate(user=self.freelancer)
        url = reverse('proposal-list')
        data = {
            'project': self.project.id,
            'cover_letter': 'I am interested',
            'bid_amount': 90
        }
        response = self.client.post(url, data)
        print("Proposal create:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_cannot_create_proposal(self):
        self.client.force_authenticate(user=self.client_user)
        url = reverse('proposal-list')
        data = {
            'project': self.project.id,
            'cover_letter': 'I am interested',
            'bid_amount': 90
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProfileTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')
        self.client.force_authenticate(user=self.user)

    def test_create_profile(self):
        url = reverse('profile-list')
        data = {
            'skills': 'Python, Django',
            'experience': '2 years',
            'portfolio': '',
            'hourly_rate': 50
        }
        response = self.client.post(url, data)
        print("Profile create:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class MessageTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.client.force_authenticate(user=self.user1)

    def test_send_message(self):
        url = reverse('message-list')
        data = {
            'receiver': self.user2.id,
            'content': 'Hello!'
        }
        response = self.client.post(url, data)
        print("Message send:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ReviewTest(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(username='client', password='pass', is_client=True)
        self.freelancer = User.objects.create_user(username='freelancer', password='pass', is_freelancer=True)
        self.project = Project.objects.create(
            client=self.client_user,
            title='Test Project',
            description='desc',
            budget=100,
            deadline='2025-12-31'
        )
        self.client.force_authenticate(user=self.client_user)

    def test_create_review(self):
        url = reverse('review-list')
        data = {
            'project': self.project.id,
            'reviewee': self.freelancer.id,
            'rating': 5,
            'comment': 'Great work!'
        }
        response = self.client.post(url, data)
        print("Review create:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)