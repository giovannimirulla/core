import traceback
import asyncio

from fastapi import APIRouter, WebSocketDisconnect, WebSocket
from cat.log import log
from fastapi.concurrency import run_in_threadpool

router = APIRouter()

# This constant sets the interval (in seconds) at which the system checks for notifications.
QUEUE_CHECK_INTERVAL = 1  # seconds


class ConnectionManager:
    """
    Manages active WebSocket connections.
    """

    def __init__(self):
        # List to store all active WebSocket connections.
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Accept the incoming WebSocket connection and add it to the active connections list.
        """

        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Remove the given WebSocket from the active connections list.
        """
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """
        Send a personal message (in JSON format) to the specified WebSocket.
        """
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        """
        Send a message to all active WebSocket connections.
        """
        for connection in self.active_connections:
            await connection.send_json(message)

    #broadcast all connections except mine
    async def broadcast_except_me(self, message: str, websocket: WebSocket):
        for connection in self.active_connections:
            if connection != websocket:
                await connection.send_json(message)


manager = ConnectionManager()


async def receive_message(websocket: WebSocket, ccat: object):
    """
    Continuously receive messages from the WebSocket and forward them to the `ccat` object for processing.
    """
    while True:
            # message received from specific user
            user_message = await websocket.receive_json()

            print("user_message",user_message)

            await manager.broadcast_except_me( {'error': False, 'type': 'chat', 'content': {'text': user_message["text"],'sender': 'user'}},websocket)

            # get response from the cat
            cat_message = await run_in_threadpool(ccat, user_message)

            # send output to specific user
            print("cat_message",cat_message)
            await manager.broadcast(cat_message)


async def check_messages(websocket: WebSocket, ccat):
    """
    Periodically check if there are any new notifications from the `ccat` instance and send them to the user.
    """
    while True:
        if ccat.ws_messages:
            # extract from FIFO list websocket notification
            notification = ccat.ws_messages.pop(0)
            await manager.send_personal_message(notification, websocket)

        # Sleep for the specified interval before checking for notifications again.
        await asyncio.sleep(QUEUE_CHECK_INTERVAL)


@router.websocket_route("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Endpoint to handle incoming WebSocket connections, process messages, and check for messages.
    """

    # Retrieve the `ccat` instance from the application's state.
    ccat = websocket.app.state.ccat

    # Add the new WebSocket connection to the manager.
    await manager.connect(websocket)

    try:
        # Process messages and check for notifications concurrently.
        await asyncio.gather(
            receive_message(websocket, ccat),
            check_messages(websocket, ccat)
        )
    except WebSocketDisconnect:
        # Handle the event where the user disconnects their WebSocket.
        log.info("WebSocket connection closed")
    except Exception as e:
        # Log any unexpected errors and send an error message back to the user.
        log.error(e)
        traceback.print_exc()
        await manager.send_personal_message({
            "type": "error",
            "name": type(e).__name__,
            "description": str(e),
        }, websocket)
    finally:
        # Always ensure the WebSocket is removed from the manager, regardless of how the above block exits.
        manager.disconnect(websocket)
