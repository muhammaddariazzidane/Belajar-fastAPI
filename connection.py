from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

client = AsyncIOMotorClient(
    # "mongodb+srv://why-media:why-media@why-media-cluster.yisdkbh.mongodb.net/why-media-db"
    "mongodb+srv://why-media:why-media@why-media-cluster.yisdkbh.mongodb.net/"
)
# database = client["why-media-db"]

# users = database["users"]
# posts = database["posts"]
# comments = database["comments"]

engine = AIOEngine(client=client, database="why-media-db")

# print(engine.find_one())
