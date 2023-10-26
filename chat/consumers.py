import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join Room Group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]

        # send message to websocket
        await self.send(text_data=json.dumps({"message": message}))

    # ASYNCHRONOUS CODE:

    # CURRENTY SYNCHRONOUS CODE:

    # class ChatConsumer(WebsocketConsumer):
    #     def connect(self):
    #         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
    #         self.room_group_name = f"chat_{self.room_name}"

    #         # join room group
    #         async_to_sync(self.channel_layer.group_add)(
    #             self.room_group_name, self.channel_name
    #         )
    #         self.accept()

    #     def disconnect(self, close_code):
    #         # Leave room group
    #         async_to_sync(self.channel_layer.group_discard)(
    #             self.room_group_name, self.channel_name
    #         )

    #     # recieve message from websocket
    #     def receive(self, text_data=None, bytes_data=None):
    #         text_data_json = json.loads(text_data)
    #         message = text_data_json["message"]

    #         # send message to the group
    #         async_to_sync(self.channel_layer.group_send)(
    #             self.room_group_name,
    #             {
    #                 "type": "chat.message",
    #                 "message": message,
    #             },
    #         )

    # recieve message from group room
