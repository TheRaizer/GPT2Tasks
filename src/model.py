from transformers import GPT2Tokenizer
from optimum.onnxruntime import ORTModelForCausalLM


class LanguageModel:
    def __init__(
        self,
        model_path: str,
    ):
        self.model: ORTModelForCausalLM = ORTModelForCausalLM.from_pretrained(
            model_path
        )
        self.tokenizer: GPT2Tokenizer = GPT2Tokenizer.from_pretrained(model_path)

    def generate_text(
        self, prompt: str, max_length: int, num_return_sequences: int = 1
    ):
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")

        outputs = self.model.generate(
            input_ids=input_ids,
            do_sample=True,
            max_length=max_length,
            top_p=0.92,
            top_k=50,
            num_return_sequences=num_return_sequences,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        sequences = []
        for sequence in outputs:
            decoded_sequence = self.tokenizer.decode(sequence)
            sequences.append(decoded_sequence)

        return sequences
