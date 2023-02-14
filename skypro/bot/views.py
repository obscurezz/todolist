from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient
from skypro.settings import env


class TgVerificationView(GenericAPIView):
    model = TgUser
    serializer_class = TgUserSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs) -> Response:
        serializer: TgUserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tg_user: TgUser = serializer.validated_data['tg_user']
        tg_user.user = self.request.user
        tg_user.save(update_fields=('user',))

        instance_serializer: TgUserSerializer = self.get_serializer(tg_user)
        TgClient(env.str('TG_TOKEN')).send_message(tg_user.tg_chat_id, '[verification_completed]')
        return Response(instance_serializer.data)
