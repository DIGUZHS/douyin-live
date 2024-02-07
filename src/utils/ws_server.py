import asyncio
import websockets

connected_clients = []


async def handle_client(websocket, path):
    connected_clients.append(websocket)
    try:
        async for message in websocket:
            print(f"Received from {websocket}: {message}")

            # 广播消息到所有连接的客户端
            for client in connected_clients:
                if client is not websocket:  # 不给自己发送消息
                    await client.send(f"{message}")

            # 检查某个特定条件，并向所有客户端发送消息
            if message == "some condition":
                for client in connected_clients:
                    await client.send("Server initiated message")
    except websockets.exceptions.ConnectionClosedError:
        pass
    finally:
        connected_clients.remove(websocket)


async def start_server():
    async with websockets.serve(handle_client, "localhost", 8080):
        await asyncio.Future()


asyncio.run(start_server())
