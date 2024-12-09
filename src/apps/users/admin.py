from django.contrib import admin

from .models import User, UserProfile, ProhibitedWord


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """사용자 관리자 페이지"""

    list_display = [
        "email",
        "is_staff",
        "is_active",
        "date_joined",
    ]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """프로필 관리자 페이지"""

    list_display = [
        "user",
        "nickname",
        "introduction",
        "avatar",
        "scopes",
        "created_at",
        "updated_at",
    ]


@admin.register(ProhibitedWord)
class ProhibitedWordAdmin(admin.ModelAdmin):
    """금지어 관리자 페이지"""

    list_display = [
        "word",
        "created_at",
    ]
