from rest_framework.viewsets import ModelViewSet
from apps.reviews.models import Review
from apps.reviews.api.serializer import ReviewSerializer
from apps.reviews.api.permissions import IsReviewOwner


class ReviewApiViewSet(ModelViewSet):
    permission_classes = [IsReviewOwner]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)