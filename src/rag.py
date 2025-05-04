from qdrant_client import models, QdrantClient
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from sentence_transformers import SentenceTransformer

load_dotenv()

client = QdrantClient(url="http://localhost:6333")
encoder = SentenceTransformer("all-MiniLM-L6-v2")



def clean_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    convos = list()
    convo = list()
    for i in range(len(data)):
        if len(convo) > 1:
            convos.append(convo.copy())
            convo.clear()
        else:
            convo.append(data[i])
    with open("user_data.json", "w") as ff:
        json.dump(convos, ff, indent=4)


def upload_vectors():
    with open("user_data.json",'r') as f:
        data = json.load(f)
    embeddings = encoder.encode(data)
    vector_size = len(embeddings[0])


    client.create_collection(
        collection_name="user_data_new",
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE,
        ),
    )
    points = []
    count = 0
    for id, embedding in enumerate(zip(embeddings,data)):
        data = list(embedding)
        payload = {}
        for i, d in enumerate(data[1]):
            payload[f"{count}"] = d
            count += 1
        
        # print(f"ID : {id}, Embedding : {data[0].tolist()}, payload : {payload}" )
        # print("-------------------------------------------------------------------")
        points.append(
            models.PointStruct(
                id=id,
                vector=data[0].tolist(),
                payload=payload
            )
        )
    client.upload_points(
        collection_name="user_data_new",
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


def rag(question: str, n_points: int = 5) -> str:
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
        collection_name="user_data_new",
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

rag("where does the user live?")

print("hello world")


