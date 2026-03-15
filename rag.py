from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import config

openai_client = AzureOpenAI(
    api_key=config.AZURE_OPENAI_KEY,
    azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
    api_version="2024-02-15-preview"
)

search_client = SearchClient(
    endpoint=config.SEARCH_ENDPOINT,
    index_name=config.SEARCH_INDEX,
    credential=AzureKeyCredential(config.SEARCH_KEY)
)

def retrieve_documents(question):

    results = search_client.search(
        search_text=question,
        top=3
    )

    docs = [r["content"] for r in results]

    return "\n".join(docs)


def ask(question):

    docs = retrieve_documents(question)

    prompt = f"""
Use the documentation below to answer.

Documentation:
{docs}

Question:
{question}
"""

    response = openai_client.chat.completions.create(
        model=config.CHAT_MODEL,
        messages=[
            {"role":"system","content":"You are a Citrix troubleshooting assistant."},
            {"role":"user","content":prompt}
        ]
    )

    return response.choices[0].message.content