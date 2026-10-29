from django.contrib.auth import get_user_model
from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny
from django.db.models import Count
from .models import ReadingMaterials, Ratings
from .serializers import ReadingMaterialsSerializer, UserSerializer, RatingsSerializer

User = get_user_model()


# ==================================================
# READING MATERIALS
# ==================================================

# GET: List all materials
# POST: Add a new material
class ReadingMaterialsListCreateView(generics.ListCreateAPIView):
    queryset = (
        ReadingMaterials.objects
        .annotate(
            student_count=Count("ratings__student", distinct=True)
        )
        .order_by("-date_added")
    )
    serializer_class = ReadingMaterialsSerializer
    permission_classes = [AllowAny]


# GET: Retrieve one material
# PUT/PATCH: Edit a material
# DELETE: Delete a material
class ReadingMaterialsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReadingMaterials.objects.annotate(
        student_count=Count("ratings__student", distinct=True)
    )
    serializer_class = ReadingMaterialsSerializer
    permission_classes = [AllowAny]


# GET: Retrieve one material
# PUT/PATCH: Edit a material
# DELETE: Delete a material
class ReadingMaterialsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReadingMaterials.objects.all()
    serializer_class = ReadingMaterialsSerializer
    permission_classes = [AllowAny]


# ==================================================
# USERS
# ==================================================

# GET: List users (latest first)
class UserListView(generics.ListAPIView):
    queryset = User.objects.exclude(
        is_staff=True,
        is_superuser=True
    ).order_by("-id")
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# POST: Create a user with an automatically generated username/password
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# PUT/PATCH: Edit a user's full name only
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name"]


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [AllowAny]


# DELETE: Delete a user
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    

class RatingsListCreateView(generics.ListCreateAPIView):
    queryset = Ratings.objects.select_related(
        "student",
        "material_title"
    ).order_by("-created")

    serializer_class = RatingsSerializer

    # Change this to IsAuthenticated if your API requires login.
    permission_classes = [AllowAny]
