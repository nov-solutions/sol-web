#!/usr/bin/env python3
import aws_cdk as cdk
from decouple import config

from cdk.web_stack import WebStack

SITE_NAME = config("NEXT_PUBLIC_SITE_NAME")
account = config("CDK_ACCOUNT")
region = config("CDK_REGION")

app = cdk.App()

env = cdk.Environment(
    account=account,
    region=region,
)

WebStack(
    app,
    SITE_NAME + "WebStack",
    env=env,
)

app.synth()
