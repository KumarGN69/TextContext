from sentence_transformers import SentenceTransformer, util
from custom_llm import LLMModel
from loguru import logger


model = LLMModel()
client = model.getclientinterface()

content1 = client.generate(
    model="llama3.2",
    prompt="Who is the current president of United states of America"
)
logger.info(content1.response)
content2 = client.generate(
    model="llama3.2",
    prompt="Who is the current president of United states of America"
)
logger.info(content2.response)
transformer_model = SentenceTransformer("deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
transformer_model.save("./deepseek-R1-Zero")
transformer_local_model = SentenceTransformer("./deepseek-R1-Zero")



content1_emb = transformer_local_model.encode(content1.response, convert_to_tensor=True)
content2_emb = transformer_local_model.encode(content2.response, convert_to_tensor=True)

content1_sim = util.pytorch_cos_sim(content1_emb, content2_emb).item()

print(f"content1 vs content2 similarity: {content1_sim: .4f}")
