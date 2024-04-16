#!/usr/bin/env python3
import aws_cdk as cdk
from decouple import config

from cdk.deploy_stack import DeployStack
from cdk.web_stack import WebStack

SITE_NAME = config("SITE_NAME")

app = cdk.App()

env = cdk.Environment(
    account="TODO",
    region="us-west-2",
)

WebStack(
    app,
    SITE_NAME + "WebStack",
    env=env,
)

DeployStack(
    app,
    SITE_NAME + "DeployStack",
    env=env,
)


app.synth()
