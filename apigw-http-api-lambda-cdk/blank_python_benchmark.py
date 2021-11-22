"""Simple hello world Python example based on the serverless pattern:
Amazon API Gateway to AWS Lambda: https://serverlessland.com/patterns/apigw-http-lambda-cdk

IMPORTANT: HTTP APIs do NOT support X-Ray, only REST APIs do!
"X-Ray only supports tracing for REST APIs through API Gateway."
Source: https://docs.aws.amazon.com/xray/latest/devguide/xray-services-apigateway.html
"""

import logging
import json
import os


BENCHMARK_CONFIG = """
blank_python:
  description: Empty Python Lambda function
  provider: aws
  region: us-east-1
"""

CDK_IMAGE = 'python-node-cdk-blank-python'
# Manual flag to bootstrap CDK. Optionally disable after first run.
BOOTSTRAP_CDK = True


def prepare(spec):
    spec.build(CDK_IMAGE)
    # Only required once per region: https://docs.aws.amazon.com/cdk/latest/guide/bootstrapping.html
    # No automated cleanup: https://github.com/aws/aws-cdk/issues/986
    if BOOTSTRAP_CDK:
        spec['account_id'] = spec.run('aws sts get-caller-identity --query Account --output text', image='aws_cli').strip()
        bootstrap_cmd = f"cdk bootstrap aws://{spec['account_id']}/{spec['region']}"
        spec.run(bootstrap_cmd, image=CDK_IMAGE)
    spec.run(f"AWS_REGION={spec['region']} cdk deploy --require-approval never --outputs-file outputs.json", image=CDK_IMAGE)
    with open('outputs.json') as f:
        outputs = json.load(f)
        spec['endpoint'] = outputs['ApigwHttpApiLambdaStack']['APIEndpoint']
        logging.info(f"service endpoint={spec['endpoint']}")


def invoke(spec):
    envs = {
        'URL': spec['endpoint']
    }
    spec.run_k6(envs)
    # Alternative invocation through curl:
    # spec.run(invoke_curl_cmd(spec['endpoint']), image='curlimages/curl:7.80.0')


def invoke_curl_cmd(url):
    return f"""curl -H "Origin: https://www.example.com" "{url}?path=parameter" --verbose"""


def cleanup(spec):
    spec.run('cdk destroy --force', image=CDK_IMAGE)
