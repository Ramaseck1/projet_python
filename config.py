from pymongo import MongoClient
import redis

def get_mongo_collection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["gestion_etudiant"]
    return db["etudiants"]

def get_redis_client():
    return redis.Redis(host='localhost', port=6379, db=0)
