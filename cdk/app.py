#!/usr/bin/env python3

import aws_cdk as cdk

from cdk.web_stack import WebStack

CDK_ACCOUNT = "844884166370"
CDK_REGION = "us-west-2"
SITE_NAME = "TODO"

app = cdk.App()

env = cdk.Environment(
    account=CDK_ACCOUNT,
    region=CDK_REGION,
)

WebStack(
    app,
    SITE_NAME + "WebStack",
    env=env,
)

app.synth()
