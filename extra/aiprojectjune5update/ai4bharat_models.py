import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from torch.nn.functional import cosine_similarity
import os 

os.environ["TRANSFORMERS_OFFLINE"] = "1"
# Load RomanSetu (romanized CPT model)
model_path = "ai4bharat/romansetu-cpt-roman-200m"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, output_hidden_states=True)
model.eval()

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # Use last hidden state, mean-pool across tokens
    hidden = outputs.hidden_states[-1]  # (1, seq_len, hidden_dim)
    mask = inputs["attention_mask"].unsqueeze(-1)
    embedding = (hidden * mask).sum(dim=1) / mask.sum(dim=1)
    return embedding.squeeze()

text_en = """India is a country of incredible diversity. From the snow-capped mountains 
of the Himalayas in the north to the tropical beaches of Kerala in the south, 
the landscape changes dramatically. Cricket is not just a sport here, it is a religion."""

text_hi = """Bharat ek adbhut vividhata wala desh hai. Uttar mein Himalaya ki baraf se 
dhaki chotiyon se lekar dakshin mein Kerala ke tropical beaches tak, yahan 
ka bhoomiparsh natak ki tarah badalta hai. Cricket yahan sirf ek khel nahi hai, 
yeh ek dharm hai."""

emb_en = get_embedding(text_en)
emb_hi = get_embedding(text_hi)

sim = cosine_similarity(emb_en.unsqueeze(0), emb_hi.unsqueeze(0)).item()
print(f"RomanSetu embedding similarity: {sim:.4f}")
