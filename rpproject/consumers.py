from channels.generic.websocket import AsyncWebsocketConsumer

class RpGameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data):
        # handle incoming data
        await self.send(text_data=f"Received: {text_data}")

