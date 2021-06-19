from typing import Mapping
import torch
import logging
from transformers import DistilBertTokenizerFast

from movie_prediction.models import DistilBertForPrincipalPrediction
from movie_prediction.constants import (
    HUGGINGFACE_PRETRAINED, TOKENIZER_ARGS_DEFAULT,
    PRINC_PRED_MODEL_TUNED_INF, MODEL_DIR
)

__all__ = ['DistilBertForPrincipalPredictionWrapper']


class DistilBertForPrincipalPredictionWrapper:
    """
    Wrapper class for loading and serving the Principal Prediction Model
    """

    def __init__(self):
        self.model_path = MODEL_DIR + '/' + PRINC_PRED_MODEL_TUNED_INF
        logging.info(f"Loading model from {self.model_path}...")
        self.tokenizer = DistilBertTokenizerFast.from_pretrained(HUGGINGFACE_PRETRAINED)
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

        self.model = DistilBertForPrincipalPrediction.from_pretrained(self.model_path)
        self.model.to(self.device)
        self.model.eval()

    def predict(self, utt: str) -> Mapping[str, float]:
        """
        Given an utterance text return the predicted probabilities of what actors said it.
        :param utt: str
            The utterance text to classify.
        :return:
            Mapping[str, float]
            A mapping between each principal and their softmax probabilities in the model.
        """
        # Tokenize Ids
        input_ids, attention_mask = self.tokenizer([utt], **TOKENIZER_ARGS_DEFAULT).values()

        # Send to backend
        input_ids = torch.tensor(input_ids).to(self.device)
        attention_mask = torch.tensor(attention_mask).to(self.device)

        # Predict Principal
        predicted_output = self.model(input_ids, attention_mask)
        predicted_output = torch.softmax(predicted_output[0].squeeze(), dim=0)

        # Extract prediction and beautify
        predicted_output = predicted_output.cpu().detach().tolist()
        predicted_output = {
            self.model.config.id2label[i]: v
            for i, v in enumerate(predicted_output)
        }
        predicted_output = {
            k: v for k, v in sorted(
                predicted_output.items(), key=lambda x: x[1],
                reverse=True)
        }

        return predicted_output
