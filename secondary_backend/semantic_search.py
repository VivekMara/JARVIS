from qdrant_client import models, QdrantClient
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from sentence_transformers import SentenceTransformer

load_dotenv()

client = QdrantClient(url="http://localhost:6333")
encoder = SentenceTransformer("all-MiniLM-L6-v2")

def upload_vectors():
    with open("data.json",'r') as f:
        data = json.load(f)
    msgs = data['messages']
    texts_to_embed = [f"{i["role"]} : {i["content"]}" for i in msgs]
    embeddings = encoder.encode(texts_to_embed)
    vector_size = len(embeddings[0])
    client.create_collection(
        collection_name="user_data",
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE,
        ),
    )
    points = []
    for id, embedding in enumerate(zip(embeddings,msgs)):
        idx = id
        data = list(embedding)
        # print(f"ID : {idx}, Embedding : {data[0].tolist()}, payload : {data[1]}" )
        # print("-------------------------------------------------------------------")
        points.append(
            models.PointStruct(
                id=idx,
                vector=data[0].tolist(),
                payload=data[1]
            )
        )
    client.upload_points(
        collection_name="user_data",
        points=points
    )


apiKey = os.getenv("deepseek_api_key")
deepseek_client = OpenAI(api_key=apiKey, base_url="https://api.deepseek.com")

def query_deepseek(prompt):
    resp = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        stream=False
    )

    print(resp.choices[0].message.content)


def rag(question: str, n_points: int = 10) -> str:
    resp = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role":"system",
                "content":"You are an helpful assistant who has to extract keywords from the input text from the user and give the resut in a neat comma seperated output. It is essential that you output just the keywords and not any other word except those keywords."
            },
            {
                "role" : "user",
                "content" : question
            }
        ],
        stream=False
    )
    keywords = resp.choices[0].message.content
    print(keywords)
    print("------------------------------------------------------")
    results = client.query_points(
        collection_name="user_data",
        query=encoder.encode(keywords).tolist(),
        limit=n_points,
    ).points
    context = []
    for i in results:
        context.append({
            "relevance_score" : i.score,
            "payload" : i.payload
        })
    metaprompt = f"""
    You are an helpful assistant. 
    Answer the following question using the provided context.
    Each part of the context has two parts, one is the relevance score and this score represents the relevancy of the query, higher the score better the relevance. Using which part of the context depends on you.The payload represents the conversation, role here represents the user or the assistant and assistant conversation represents you.
    The context provided is a conversation between the user and the assistant. 
    If you can't find the answer, do not pretend you know it, but only answer "I don't know".
    Do not mention to the user that you have context.

    Question: {question.strip()}
    
    Context: 
    {context}
    
    Answer:
    """
    print(metaprompt)
    return query_deepseek(metaprompt)

rag("does the user love the assistant?")