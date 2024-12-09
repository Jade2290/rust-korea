from html import escape

from rest_framework import serializers

from apps.users.models import UserProfile, ProhibitedWord


class UserProfileSerializer(serializers.ModelSerializer):
    """사용자 프로필 시리얼라이저"""

    def validate_nickname(self, attr):
        # 금지어 필터링
        if ProhibitedWord.validate_word(attr):
            raise serializers.ValidationError("닉네임에 금지어가 포함되어 있습니다.")
        # 4자에서 20자 사이
        if not 4 <= len(attr) <= 20:
            raise serializers.ValidationError(
                "닉네임은 4자에서 20자 사이로 입력해주세요."
            )
        return attr

    def validate_introduction(self, attr):
        if not attr:
            return None
        return escape(attr, quote=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "nickname",
            "introduction",
            "avatar",
            "scopes",
        ]
