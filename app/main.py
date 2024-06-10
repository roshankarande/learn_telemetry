from typing import Optional
from fastapi import FastAPI
from random import randint
import random
from time import sleep
from fastapi import HTTPException, status
from loguru import logger
import asyncio
import requests
# ========================================================================
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.trace.status import Status, StatusCode

tracer = trace.get_tracer("diceroller.tracer")


# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import (
#     BatchSpanProcessor,
#     ConsoleSpanExporter,
# )

# provider = TracerProvider()
# processor = BatchSpanProcessor(ConsoleSpanExporter())
# provider.add_span_processor(processor)

# # Sets the global default tracer provider
# trace.set_tracer_provider(provider)

# # Creates a tracer from the global tracer provider
# tracer = trace.get_tracer("my.tracer.name")

# =========================================================================

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
def read_root():
    # Create a custom span
    # with tracer.start_as_current_span("custom-span"):
        # Your code here
        return {"message": "Hello, World!"}


@app.get("/rolldice")
def roll_dice():
    return str(roll())

def roll():
    # This creates a new span that's the child of the current one
    with tracer.start_as_current_span("roll") as rollspan:
        res = randint(1, 6)
        rollspan.set_attribute("roll.value", res)
        return res


def hello_world():
    # sleep(2)
    return "hello world"


@app.get("/ping")
async def health_check():
    hello_world()
    return "pong"


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    if item_id % 2 == 0:
        # mock io - wait for x seconds
        seconds = random.uniform(0, 3)
        await asyncio.sleep(seconds)
    return {"item_id": item_id, "q": q}


@app.get("/invalid")
async def invalid():
    raise ValueError("Invalid ")

@app.get("/exception")
async def exception():
    try:
        raise ValueError("sadness")
    except Exception as ex:
        logger.error("---------------" + str(ex) + "---------------", exc_info=True)
        span = trace.get_current_span()

        # generate random number
        seconds = random.uniform(0, 30)

        # record_exception converts the exception into a span event. 
        exception = IOError("Failed at " + str(seconds))
        span.record_exception(exception)
        span.set_attributes({'est': True})
        # Update the span status to failed.
        span.set_status(Status(StatusCode.ERROR, "internal error"))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Got sadness")

@app.get("/external-api")
def external_api():
    seconds = random.uniform(0, 3)
    response = requests.get(f"https://httpbin.org/delay/{seconds}")
    response.close()
    return "ok"
