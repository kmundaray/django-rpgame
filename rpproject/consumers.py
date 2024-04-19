from channels.generic.websocket import AsyncWebsocketConsumer
import json

class RpGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Check if 'game_id' is in the URL route parameters
        game_id = self.scope['url_route']['kwargs'].get('game_id')
        if game_id:
            # If there is a game_id, use it to define a group name
            self.game_group_name = f'game_{game_id}'
            await self.channel_layer.group_add(
                self.game_group_name,
                self.channel_name
            )
            print(f"Added to game group: {self.game_group_name}")
        else:
            # Define a default group or handle differently if no game_id is provided
            self.game_group_name = 'default_game_group'
            await self.channel_layer.group_add(
                self.game_group_name,
                self.channel_name
            )
            print("Added to default game group")

    async def disconnect(self, close_code):
        # Leave game group
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        # Check if the action is to trigger a refresh
        if action == 'playfield_refresh':
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'game_refresh',
                }
            )

    async def game_refresh(self, event):
        # Send a refresh command to all clients in the group
        await self.send(text_data=json.dumps({
            'action': 'refresh'
        }))

