from src.model import LanguageModel
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/health", status_code=status.HTTP_200_OK)
def perform_healthcheck():
    return {"health": "Everything OK!"}


# learn to load model from onnx here https://huggingface.co/docs/optimum/exporters/onnx/usage_guides/export_a_model
# export gpt2 model to onnx like so: optimum-cli export onnx --model gpt2 gpt2_onnx/

model = LanguageModel(model_path="./gpt2_onnx")

outputs = model.generate_text("An explosion contains a sharp", 100, 3)

print(outputs)
