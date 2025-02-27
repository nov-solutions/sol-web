#!/usr/bin/env python3

import aws_cdk as cdk

from cdk.web_stack import WebStack

app = cdk.App()

env = cdk.Environment(
    account=844884166370,
    region="us-west-2",
)
# TODO
SITE_NAME = "TODO"

WebStack(
    app,
    SITE_NAME + "WebStack",
    env=env,
)

app.synth()
