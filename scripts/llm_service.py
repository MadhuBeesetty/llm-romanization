from openai import OpenAI
import numpy as np

class EmbeddingClient:

    def __init__(
        self,
        model="bge-m3",
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    ):
        self.model = model

        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    def get_embedding(self, text):

        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding

    def cosine_similarity(
        self,
        text1,
        text2,
    ):

        emb1 = np.array(
            self.get_embedding(text1)
        )

        emb2 = np.array(
            self.get_embedding(text2)
        )

        return float(
            np.dot(emb1, emb2)
            /
            (
                np.linalg.norm(emb1)
                * np.linalg.norm(emb2)
            )
        )
class LLMOllamaClient:
    def __init__(
        self,
        model,
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    ):
        self.model = model

        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    def generate(
        self,
        system_prompt,
        prompt,
        # max_tokens=512,
        temperature=0,
        repeat_penalty=1.2,
        top_p=0.9,
    ):
        """
        Generate a response using Ollama's OpenAI-compatible API.
        Returns:
            {
                response,
                reasoning,
                finish_reason,
                usage,
                model
            }
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            # max_tokens=max_tokens,
            extra_body={
                "options": {
                    "temperature": temperature,
                    "repeat_penalty": repeat_penalty,
                    "top_p": top_p,
                }
            },
        )

        choice = response.choices[0]

        return {
            "response": choice.message.content,
            "reasoning": getattr(
                choice.message,
                "reasoning",
                None,
            ),
            "finish_reason": choice.finish_reason,
            "usage": response.usage,
            "model": response.model,
        }

    def chat(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content