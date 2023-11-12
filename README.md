# RAG on AWS usign Amazon Bedrock, Amazon Kendra, Amazon Lambda Function, Amazon S3 and Amazon DynamoDB

🇻🇪🇨🇱 [Dev.to](https://dev.to/elizabethfuentes12) [Linkedin](https://www.linkedin.com/in/lizfue/) [GitHub](https://github.com/elizabethfuentes12/) [Twitter](https://twitter.com/elizabethfue12) [Instagram](https://www.instagram.com/elifue.tech) [Youtube](https://www.youtube.com/channel/UCr0Gnc-t30m4xyrvsQpNp2Q)
[Linktr](https://linktr.ee/elizabethfuentesleone)

---

In this repository you will find a use cases of RAG on AWS using [CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html). 

Additionally,  you will find a notebook where you can run the agent localy.

## What Are You Going To Learn. 

- How to create a vectordb using [Amazon Bedrock - Titan Embeddings](https://docs.aws.amazon.com/bedrock/latest/userguide/embeddings.html),  [chroma](https://www.trychroma.com/) and [langchain](https://www.langchain.com/).
- How to store the vectordb in an [Amazon S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingBucket.html).
- How to build an Agent with memory capable of following a more fluid conversation (learn more about using memories with agents [here](https://community.aws/posts/working-with-your-live-data-using-langchain))
- How to query vectordb stored in s3 bucket through a fluid conversation with langchain agent employed an LLM.
- How to query a Amazon Dynamodb table through a fluid conversation with langchain agent employed an LLM.
- How to put item to a Amazon Dynamodb table through a fluid conversation with langchain agent employed an LLM.

✅ **AWS Level**: Intermediate - 200   

💰 **Cost to complete**: 
- [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [Amazon Lambda Pricing](https://aws.amazon.com/lambda/pricing/)
- [Amazon DynamoDB Pricing](https://aws.amazon.com/dynamodb/pricing/)
- [Amazon S3](https://aws.amazon.com/s3/pricing/)

✅ **Prerequisites:**

- [AWS Account](https://aws.amazon.com/resources/create-account/?sc_channel=el&sc_campaign=datamlwave&sc_content=cicdcfnaws&sc_geo=mult&sc_country=mult&sc_outcome=acq) 
-  [Foundational knowledge of Python](https://catalog.us-east-1.prod.workshops.aws/workshops/3d705026-9edc-40e8-b353-bdabb116c89c/) 

This is a multilingual (limited to the LLM you use) agent is a spa assistant specialized in massages (with some data that I found on Google 😅... it is not very reliable), recommends types of massages based on the client's comments, schedules appointments and checks their status.

![Digrama parte 1](/imagenes/image_01.png)

## Let's build!

✅ **Clone the repo**

```
git clone https://github.com/elizabethfuentes12/aws-qa-agent-with-bedrock-kendra-and-memory.git
```

✅ **Create The DBvector Following The Code In This Notebook:** [Here](create_vectordb_data_spa.ipynb)

The dbvector will be saved within the CDK stack [/vectordb](/spa-assistant-agent/vectordb), which will create an S3 bucket with the dbvector stored in it.

✅ **Go to**: 

```
cd re-invent-agent
```

✅ **Create The Virtual Environment**: by following the steps in the [README](/re-invent-agent/README.md)

```
python3 -m venv .venv
```

```
source .venv/bin/activate
```
for windows: 

```
.venv\Scripts\activate.bat
```

✅ **Install The Requirements**:

```
pip install -r requirements.txt0
```

✅ **Synthesize The Cloudformation Template With The Following Command**:

```
cdk synth
```

✅🚀 **The Deployment**:

```
cdk deploy
```

> Play with the agent and improve the prompt, remember that he has memory storage and you can have a fluid conversation with it.


----

## 🚨 Did you like this blog? 👩🏻‍💻 Do you have comments?🎤 tell me everything [here](https://www.pulse.aws/survey/6V3IYE9H)

----

## ¡Gracias!

🇻🇪🇨🇱 [Dev.to](https://dev.to/elizabethfuentes12) [Linkedin](https://www.linkedin.com/in/lizfue/) [GitHub](https://github.com/elizabethfuentes12/) [Twitter](https://twitter.com/elizabethfue12) [Instagram](https://www.instagram.com/elifue.tech) [Youtube](https://www.youtube.com/channel/UCr0Gnc-t30m4xyrvsQpNp2Q)
[Linktr](https://linktr.ee/elizabethfuentesleone)

---


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.