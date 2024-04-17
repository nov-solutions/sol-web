from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from constructs import Construct
from decouple import config

SITE_NAME = config("SITE_NAME")


class WebStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # default vp
        vpc = ec2.Vpc.from_lookup(
            self,
            SITE_NAME + "-web-vpc",
            is_default=True,
        )

        # security group
        security_group = ec2.SecurityGroup(
            self,
            SITE_NAME + "-web-security-group",
            vpc=vpc,
            allow_all_outbound=True,
        )

        # add ingress rule for port 22
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="Allow SSH access from the Internet",
        )

        # add ingress rule for port 80
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow HTTP access from the Internet",
        )

        # add ingress rule for port 443
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(443),
            description="Allow HTTPS access from the Internet.",
        )

        # ec2 public instance
        ec2.Instance(
            self,
            SITE_NAME + "-web",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.generic_linux(
                {"us-west-2": "ami-0e4a0595b254f1a4f"}
            ),
            vpc=vpc,
            # vpc_subnets=public_subnet,
            role=iam.Role(
                self,
                SITE_NAME + "-web-ec2-role",
                assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            ),
            security_group=security_group,
            instance_name=SITE_NAME + "-web",
            key_name=SITE_NAME + "-web",
        )
