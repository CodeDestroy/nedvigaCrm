from channels.generic.websocket import AsyncJsonWebsocketConsumer


class CallConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        from django.core.exceptions import ObjectDoesNotExist
        try:
            from main.models import User
            user = await User.objects.select_related('sip').aget(pk=self.scope['user'].id)
            if user.sip:
                await self.channel_layer.group_add('call', self.channel_name)
                await self.accept()
        except ObjectDoesNotExist:
            await self.close()

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard('call', self.channel_name)

    async def show_call(self, event):
        await self.send_json(event)
