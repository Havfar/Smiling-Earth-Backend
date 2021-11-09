
from challenges.serializers import ChallengeSerializer
from posts.serializers import PostSerializer
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer
from users.serializers import ProfileSerializer

from notifications.models import Notification


class NotificationSerializer(ModelSerializer):
    # challenge = ChallengeSerializer(read_only=True)
    from_user = ReadOnlyField(source='get_from_user')
    # post = PostSerializer(read_only=True)
    # challenge = ChallengeSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ["id",
                  "to_user",
                  "from_user",
                  "notification_type",
                  "message",
                  "user_has_seen",
                  "timestamp",
                  "post",
                  "like",
                  "comment",
                  "challenge",
                  "follow"]


class CountNewNotificationSerializer(ModelSerializer):
    # challenge = ChallengeSerializer(read_only=True)
    from_user = ReadOnlyField(source='get_from_user')
    # post = PostSerializer(read_only=True)
    # challenge = ChallengeSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ["id",
                  "to_user",
                  "from_user",
                  "notification_type",
                  "message",
                  "user_has_seen",
                  "timestamp",
                  "post",
                  "like",
                  "comment",
                  "challenge",
                  "follow"]
