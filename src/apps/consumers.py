async def websocket_receive(event):
    message = event.get('text', None)
    room_id = event.get("room_id")