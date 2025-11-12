import os
import time

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

    redisStart = time.perf_counter()
    try:
        pong = await redisClient.ping()
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
    # TODO: template httpx request
    templateTime = time.perf_counter() - templateStart
    template: Dependency = Dependency(service="template-service",
                                      status="healthy",
                                      response_time_ms=int(templateTime * 1000))
    dependencies.append(template)

    healthData: HealthData = HealthData(service="user-service",
                                        status="healthy",
                                        dependencies=dependencies)

    return healthData
