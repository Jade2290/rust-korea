from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """사용자"""

    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserProfile(models.Model):
    """사용자 프로필"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField(max_length=50, unique=True, help_text="닉네임")
    introduction = models.CharField(
        max_length=255, null=True, blank=True, help_text="소개"
    )
    avatar = models.URLField(
        blank=True,
        null=True,
        help_text="프로필 이미지",
    )
    scopes = models.CharField(
        max_length=255,
        help_text="권한들",
        null=True,
        blank=True,
    )
    # 기본 설정
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_profiles"
        verbose_name = "사용자 프로필"
        verbose_name_plural = "사용자 프로필들"


class ProhibitedWord(models.Model):
    """금지어"""

    word = models.CharField(max_length=50, unique=True, help_text="금지어")
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def validate_word(cls, word: str) -> bool:
        cache_key = f"prohibited_words:list:{settings.DJANGO_ENVIRONMENT}"
        cached_data = cache.get(cache_key)
        if not cached_data:
            cached_data = cls.objects.values_list("word", flat=True)
            cache.set(cache_key, cached_data, timeout=60 * 60)
        for w in cached_data:
            if w in word:
                return True
        return False

    class Meta:
        db_table = "prohibited_words"
        verbose_name = "금지어"
        verbose_name_plural = "금지어들"
