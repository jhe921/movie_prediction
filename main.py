import sys
import logging
from fastapi import FastAPI
from fastapi.logger import logger as fastapi_logger
from movie_prediction.utils import sanitize_string
from movie_prediction.wrappers import DistilBertForPrincipalPredictionWrapper

app = FastAPI()

# Setup logger
logging.getLogger("uvicorn.error").propagate = False
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup model wrapper
model_wrapper = DistilBertForPrincipalPredictionWrapper()


@app.get("/")
async def root():
    logging.info("ROOT REQUEST")
    return {"Warning": "This endpoint does nothing."}


@app.get("/principal-prediction")
async def principal_prediction(text: str):
    logging.info(f"PRINCIPAL PREDICTION REQUEST|{text}")
    return model_wrapper.predict(
        sanitize_string(text))

