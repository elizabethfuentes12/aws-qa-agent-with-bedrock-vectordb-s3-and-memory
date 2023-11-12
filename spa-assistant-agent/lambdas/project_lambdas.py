import sys

from aws_cdk import aws_lambda, Duration, aws_iam as iam

from constructs import Construct


LAMBDA_TIMEOUT = 900

BASE_LAMBDA_CONFIG = dict(
    timeout=Duration.seconds(LAMBDA_TIMEOUT),
    memory_size=128,
    tracing=aws_lambda.Tracing.ACTIVE,
    architecture=aws_lambda.Architecture.ARM_64
)

PYTHON_LAMBDA_CONFIG = dict(
    runtime=aws_lambda.Runtime.PYTHON_3_11, **BASE_LAMBDA_CONFIG
)

from layers import Layers


class Lambdas(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        COMMON_LAMBDA_CONF = dict(environment={}, **PYTHON_LAMBDA_CONFIG)

        Lay = Layers(self, 'Lay')

        self.agent = aws_lambda.Function(
            self,
            "qa-agent",
            handler="lambda_function.lambda_handler",
            layers=[Lay.chromadb_jp,Lay.langchain],
            description ="QA Agent with LangChain and Amzon Bedrock",
            code=aws_lambda.Code.from_asset("./lambdas/code/agent"),
            **COMMON_LAMBDA_CONF
        )

        self.dynamodb_put_item = aws_lambda.Function(
            self, "DynamoDB_put_item", 
            description ="Put items to DynamoDB" ,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset("./lambdas/code/dynamodb_put_item"),
            **COMMON_LAMBDA_CONF)
        
        self.dynamodb_query = aws_lambda.Function(
            self, "query_dynamodb_passanger", 
            description ="Query DynamoDB" ,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset("./lambdas/code/dynamodb_query"),
            **COMMON_LAMBDA_CONF)
