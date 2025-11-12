import os
import time

import httpx
import redis
from fastapi import FastAPI

from .models import Dependency, HealthData

app = FastAPI()

# Connect to redis
redisClient = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)


# Endpoints
@app.get("/health")
async def health_check():
    dependencies = []
    redisStatus = ""
    templateStatus = ""

    redisStart = time.perf_counter()
    try:
        pong = redisClient.ping()
        if pong:
            redisStatus = "healthy"
        else:
            redisStatus = "unhealthy"
    except Exception as e:
        redisStatus = "unhealthy"
    redisTime = time.perf_counter() - redisStart

    redis: Dependency = Dependency(service="redis",
                                   status=redisStatus,
                                   response_time_ms=int(redisTime * 1000))
    dependencies.append(redis)

    templateStart = time.perf_counter()
    async with httpx.AsyncClient() as client:
        resp = await client.get(f'http://template-service:8000/health')
    print(resp.content)
    if resp.status_code == 200:
        templateStatus = "healthy"
    else:
        templateStatus = "unhealthy"
    templateTime = time.perf_counter() - templateStart
    template: Dependency = Dependency(service="template-service",
                                      status=templateStatus,
                                      response_time_ms=int(templateTime * 1000))
    dependencies.append(template)

    healthData: HealthData = HealthData(service="user-service",
                                        status="healthy",
                                        dependencies=dependencies)

    return healthData
