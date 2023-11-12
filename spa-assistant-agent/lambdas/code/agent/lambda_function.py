import os
import boto3
import json
import subprocess
import sys
import errno

from langchain.embeddings import BedrockEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory
from langchain.chains.conversation.memory import  ConversationSummaryMemory, ConversationBufferMemory

#subprocess.call('pip install -U chromadb -t /tmp/ --no-cache-dir'.split())

from langchain.vectorstores import Chroma

subprocess.call('pip3 install --U boto3 -t /tmp/ --no-cache-dir'.split())

from langchain.llms.bedrock import Bedrock

bedrock_client = boto3.client("bedrock-runtime")
model_parameter = {"temperature": 0.0, "top_p": .9, "max_tokens_to_sample": 2000}
bedrock_embedding_model_id = os.environ.get("EMBEDDING_MODEL")
model_llm_id = os.environ.get("LLM_MODEL")
bucket_name = os.environ.get("BUCKET_NAME")
table_name = os.environ.get('TABLE_SESSION')

persist_directory = '/tmp/docs/chroma/'
client = boto3.client('s3')

def download_file(bucket, key, filename):
    with open(filename, "wb") as data:
        client.download_fileobj(bucket, key, data)
    print("Download file from s3://{}{}".format(bucket,key))
    return True

def sync_s3_data(objects):
    for n in objects['Contents']:
        print(n["Key"], len(n["Key"].split("/")))
        path = ""
        len_int = len(n["Key"].split("/"))-1
        possition = 0
        for k in n["Key"].split("/"):
            if possition == len_int:
                break
            path = path+"/"+k
            possition += 1
        path = path.lstrip("/")
        print(path)
        try:
            os.makedirs("/tmp/"+path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        filename = "/tmp/"+ path +"/" + n["Key"].split("/")[-1]
        download_file(bucket_name, n['Key'],filename)

objects = client.list_objects(Bucket=bucket_name,Prefix="vectordb/docs")
sync_s3_data(objects)

for n in objects['Contents']:
        print(n['Key'])
        download_file(bucket_name, n['Key'], n['Key'])

def create_langchain_vector_embedding_using_bedrock(bedrock_client, bedrock_embedding_model_id):
    bedrock_embeddings_client = BedrockEmbeddings(
        client=bedrock_client,
        model_id=bedrock_embedding_model_id)
    return bedrock_embeddings_client

bedrock_embeddings_client = create_langchain_vector_embedding_using_bedrock(bedrock_client, bedrock_embedding_model_id) 

llm = Bedrock(model_id=model_llm_id, model_kwargs=model_parameter,client=bedrock_client)
#table_name = os.environ.get("TABLE_NAME")

def memory_dynamodb(id,table_name_session,llm):
    message_history = DynamoDBChatMessageHistory(table_name=table_name_session, session_id=id)
    memory = ConversationBufferMemory(
        memory_key="chat_history", llm=llm,max_token_limit=800,chat_memory=message_history, return_messages=True,ai_prefix="A",human_prefix="H"
    )
    return memory

def build_prompt():
    prompt_template = """Human: Are you a spa assistant specializing in massages, you are very talkative and provides specific details so that the human can decide what answer is best for him.
    Use the following format:
        Question: the input question you must answer
    
    Assistant: OK, got it, I'll be a talkative truthful AI assistant.

    Human: Search this question in your documents: {question}

    Assistant: Here are some documents in <documents> tags that refer to what you are talking about :
    <documents>
    {context}
    </documents>
    Human: 
    Based on the above documents, give me detailed information so I can decide about: {question}.
    Answer "don't know" if documents are empty. 
    DON'T INVENT HYPOTHETICAL ANSWERS, uses ONLY metadata in {context}. 
    Final Answer: always reply in the original user language and human legible.

    Helpful Answer:"""

    updated_prompt = PromptTemplate(
    input_variables=[ 'question', 'context'], template=prompt_template)

    return updated_prompt

def Retrieval_QA(updated_prompt,vectordb):
    qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectordb.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs={"prompt": updated_prompt},
    verbose=True,   
)
    return qa_chain

def lambda_handler(event, context):
    '''Handle Lambda event from AWS'''
    print(event)

    prompt = event['prompt']
    #session_id = event['session_id']

    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=bedrock_embeddings_client
    )

    agent = Retrieval_QA(build_prompt(),vectordb)
    completion  = agent({"query": prompt})

    print(completion['result'])
    return completion['result']



