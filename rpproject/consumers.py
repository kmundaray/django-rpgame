from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import json
import logging
logger = logging.getLogger(__name__)

# brew install redis
# brew services start redis
# brew services list
# redis-cli ping

class RpGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Check if 'game_id' is in the URL route parameters
        game_id = self.scope['url_route']['kwargs'].get('game_id')
        print(f"Game ID: {game_id}")
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
        while True:
            try:
                await asyncio.sleep(3)  # Send a heartbeat every few seconds
                await self.send(json.dumps({'type': 'heartbeat'}))
                await self.channel_layer.group_send(
                        self.game_group_name,
                        {
                            'type': 'game_refresh',
                        }
                    )
            except asyncio.CancelledError:
                break

    async def disconnect(self, close_code):
        logger.debug('Disconnected with close_code: %s', close_code)
        # Leave game group
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            try:
                text_data_json = json.loads(text_data)
                action = text_data_json.get('action')
                action_type = text_data_json.get('type')
                # Check if the action is to trigger a refresh
                print(f"Received action: {text_data_json}")
                if action == 'playfield_refresh':
                    await self.channel_layer.group_send(
                        self.game_group_name,
                        {
                            'type': 'game_refresh',
                        }
                    )
                if action_type == 'heartbeat':
                    await self.send(text_data=json.dumps({
                        'type': 'heartbeat'
                    }))
            except json.JSONDecodeError:
                print("Received malformed data:", text_data)
        else:
            print("Received an empty message.")


    async def game_refresh(self, event):
        # Send a refresh command to all clients in the group
        await self.send(text_data=json.dumps({
            'action': 'refresh'
        }))

