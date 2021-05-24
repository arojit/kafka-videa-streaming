from kafka import KafkaConsumer

from aiohttp import web
import socketio

# creates a new Async Socket IO Server
sio = socketio.AsyncServer(cors_allowed_origins='*')
# Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
# instance
sio.attach(app)

# Topic the Kafka Consumer
topic = "distributed-video1"

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=['localhost:9092'])


# we can define aiohttp endpoints just as we normally
# would with no change
async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('connection')
async def connect(sid, message):
    print(sid)
    await sio.emit('message', 'hi', sid)
    for msg in consumer:
        await sio.emit('message', msg.value)


app.router.add_get('/', index)
# We kick off our server
if __name__ == '__main__':
    web.run_app(app)
