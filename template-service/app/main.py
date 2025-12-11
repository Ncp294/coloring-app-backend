import json
import logging
import os
import time
from contextlib import asynccontextmanager

import redis
from fastapi import Depends, FastAPI
from sqlmodel import Session

from .db import (close_db_connection, getSession, getTemplateById, init_db,
                 writeTemplate)
from .models import Dependency, HealthData, Template, TemplateCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    close_db_connection()

app = FastAPI(lifespan=lifespan)

# Connect to redis
redisClient = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)


# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


# Endpoints
@app.get("/health")
async def health_check():
    dependencies = []

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

    healthData: HealthData = HealthData(service="template-service",
                                        status="healthy",
                                        dependencies=dependencies)

    return healthData


# get template by ID
@app.get("/template/{user_id}/{template_id}", status_code=200)
def getTemplate(user_id: str, template_id: str, session: Session = Depends(getSession)):
    logging.info(
        f"TEMPLATE SERVICE: request received for template {template_id}")

    # check cache
    if redisClient.exists(template_id):
        value = redisClient.get(template_id)
        logging.info(f"TEMPLATE SERVICE: CACHE HIT with id {template_id}")

        if isinstance(value, str):
            data = json.loads(value)

        # type ignoring bc sql takes care of id
        template: Template = Template(template_id=template_id,
                                      user_id=data["user_id"],
                                      public=data["public"],
                                      # type: ignore
                                      img=data["img"])

        # check userID match or listed public
        if template.public or template.user_id == user_id:
            return template

    # if miss, get stored data and then cache
    logging.info(
        f"TEMPLATE SERVICE: CACHE MISS with template {template_id}: fetching from database")
    data = getTemplateById(session, template_id)
    if not data:
        logging.error(
            f'TEMPLATE SERVICE: Template {template_id} does not exist in cache or database.')
    else:
        ttl = int(os.getenv("TTL_SECONDS", 3300))
        newData = {
            "user_id": data.user_id,
            "public": data.public,
            "img": data.img
        }
        try:
            redisClient.setex(template_id, ttl, json.dumps(newData))
            logging.info(
                f'TEMPLATE SERVICE: stored data in Redis with TTL={ttl} for {template_id}')
        except Exception as e:
            logging.info(
                f'TEMPLATE SERVICE: failed to write to Redis for {template_id} ({e})')

        if data.public or data.user_id == user_id:
            return data


# add new template
@app.post("/template", status_code=201)
def addTemplate(template: TemplateCreate, session: Session = Depends(getSession)):
    newTemplate: Template = Template(template_id=template.template_id,
                                     user_id=template.user_id,
                                     public=template.public,
                                     img=template.img)  # type: ignore

    # write to db
    writeTemplate(session, newTemplate)
    logging.info(
        f"TEMPLATE SERVICE: created new DB record for {template.template_id}")

    # invalidate cache
    if redisClient.exists(template.template_id):
        try:
            redisClient.delete(template.template_id)
        except Exception as e:
            logging.error(
                f"TEMPLATE SERVICE: Redis unavailable, cannot invalidate cache for {template.template_id}. ({e})")
        logging.info(
            f"TEMPLATE SERVICE: Cache entry for {template.template_id} invalidated.")

    return newTemplate.model_dump()
