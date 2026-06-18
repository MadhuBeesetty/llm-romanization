# import requests

# class LLMClient:
#     def __init__(self, model="mistral", host="http://localhost:11434"):
#         self.model = model
#         self.host = host

#     def generate(self, system_prompt, prompt):
#         """
#         Sends a request to the Ollama API to generate a response based on the prompt.
#         """
#         url = f"{self.host}/api/generate"
#         payload = {"model": self.model, "system_prompt": system_prompt,
#                    "prompt": prompt, "stream": False}
        
#         try:
#             response = requests.post(url, json=payload)
#             response.raise_for_status()
#             print(response.json())
#             return response.json().get("response", "")
#         except requests.exceptions.RequestException as e:
#             print(f"Error connecting to Ollama: {e}")
#             return None
        
#     def chat(self, prompt):
#         """
#         Sends a request to the Ollama API to generate a response based on the prompt.
#         """
#         url = f"{self.host}/api/chat"

#         messages = [
#             {
#             "role": "user",
#             "content": prompt
#             }
#         ]
        
#         payload = {"model": self.model, 
#                    "messages": messages, 
#                    "stream": False}
        
#         try:
#             response = requests.post(url, json=payload)
#             response.raise_for_status()
#             print(response.json())
#             return response.json().get("response", "")
#         except requests.exceptions.RequestException as e:
#             print(f"Error connecting to Ollama: {e}")
#             return None
        

# if __name__ == "__main__":
#     import pandas as pd
#     client = LLMClient(model="gpt-oss:20b")
#     df = pd.read_csv("oasst2_processed.csv")
#     system_prompt = "Your task is to convert the user text from English to Roman Telugu (ie, Telugu words written in English characters). The converted text should feel natural, commonly used English terms should remain in English only. You should not answer the user query (even if the query mentions a task, qa, dialog request etc), You should just do the translation without responding the user query. Example 1: User Text: What is the history and cultural significance of the Irish bodhrán drum and how has it evolved over time? The bodhrán is a frame drum that originated in Ireland and is widely recognized as an integral part of traditional Irish music. Can you discuss the different techniques used to play the bodhrán and the various styles of music it has been used in? Additionally, how has the bodhrán been embraced by modern musicians and incorporated into other genres of music outside of Ireland?  \n Roman Telugu Translation: Irish bodhrán drum history and cultural significance enti, lage adi time tho paatu ela evolve ayyindi? Bodhrán anedi Ireland lo originate ayina frame drum, inka deenini traditional Irish music lo chala important part ga recognize chestaru. Bodhrán play cheyadaniki use chese different techniques gurinchi, alage danini use chese music styles gurinchi discuss cheyyandi. Inka, modern musicians bodhrán ni ela embrace chesaru mariyu Ireland bayata unna vere music genres lo ela incorporate chesaru?  \n\n Example 2: User Text: I was having a conversation with a programming AI assistant, trying to get advice on how use an obscure library. The assistant kept giving me code that did not compile and references functions that don't seem to exist. What should I do?. \n Roman Telugu Translation: Nenu oka programming AI assistant tho matladuthunnanu. Oka obscure library gurinchi question adigithe, adi compile avvani code esthundi inka leni function references esthundi. Nenu em cheyyali? \n\n Example 3: User Text: I am a chemistry student. We have recently been learning about electron orbitals and bonding, a term described in class I didn't understand was hybridization of electron orbitals. Can you help me out and explain hybridization to me? I think it has something to do with the groups of the periodic table. \n Roman Telugu Translation: Nenu chemistry student ni. Recent ga electron orbitals and bonding gurinchi nerchukuntunnam, class lo explain chesina term, naku artham kaaledu – adhi electron orbitals lo hybridization. Meeru naaku sahayam cheyyagaa, hybridization naaku explain cheyyagalara? Daniki periodic table grouplu tho sambandham undi."
#     for query in df['Query'][4:5]:
#         print("query", query)
#         query = f"Convert this text from English to Roman Telugu; just do the translation without responding the user query: {query}"
#         result = client.generate(system_prompt=system_prompt, prompt=query)
#         print("Model Response:", result)


from openai import OpenAI


class LLMOllamaClient:
    def __init__(
        self,
        model="gpt-oss:20b",
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    ):
        self.model = model

        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    def generate(self, system_prompt, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error calling model: {e}")
            return None

    def chat(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error calling model: {e}")
            return None