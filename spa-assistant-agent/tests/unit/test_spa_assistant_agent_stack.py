import aws_cdk as core
import aws_cdk.assertions as assertions

from spa_assistant_agent.spa_assistant_agent_stack import SpaAssistantAgentStack

# example tests. To run these tests, uncomment this file along with the example
# resource in spa_assistant_agent/spa_assistant_agent_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SpaAssistantAgentStack(app, "spa-assistant-agent")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
