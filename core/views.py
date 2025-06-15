from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import stripe

from .models import User, Profile, Project, Proposal, Message, Review
from .serializers import (
    UserSerializer, ProfileSerializer, ProjectSerializer, ProposalSerializer,
    MessageSerializer, ReviewSerializer
)
from .permissions import IsFreelancer, IsClient

# Registration view
from rest_framework.permissions import AllowAny

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_client:
            return Project.objects.filter(client=user)
        return Project.objects.filter(is_open=True)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated, IsFreelancer]

    def get_queryset(self):
        return Proposal.objects.filter(freelancer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(freelancer=self.request.user)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(reviewer=user) | Review.objects.filter(reviewee=user)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

class CreatePaymentIntentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(float(amount) * 100),  # Stripe expects amount in cents
                currency='usd',
                metadata={'user_id': request.user.id},
                api_key=settings.STRIPE_SECRET_KEY
            )
            return Response({'clientSecret': intent['client_secret']})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)