from google.cloud import aiplatform_v1beta1 as aiplatform
import numpy as np

PROJECT_ID = "<GCP Project ID"
LOCATION = "us-central1"
MODEL_ID = "gemini-embedding-001" # supported text embedding model
ENDPOINT = f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL_ID}"


def get_embedding_model():
    return None


def embed_text_chunks(chunks, _model=None, batch_size=1):
    client = aiplatform.PredictionServiceClient(
        client_options={"api_endpoint": f"{LOCATION}-aiplatform.googleapis.com"}
    )

    embeddings = []
    for chunk in chunks:
        instance = {"content": chunk}
        response = client.predict(
            endpoint=ENDPOINT,
            instances=[instance],
            timeout=60.0,
        )
        # Extract the embedding values
        embeddings.append(response.predictions[0]["embeddings"]["values"])

    return chunks, np.array(embeddings)
