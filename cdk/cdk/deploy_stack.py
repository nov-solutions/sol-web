import json

from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_efs as efs
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_secretsmanager as sm
from constructs import Construct


class DeployStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "NEWSOLWEBAPPDeployVPC")
        # elastic file system for container file mounting
        file_system = efs.FileSystem(self, "NEWSOLWEBAPPEfs", vpc=vpc)

        # this is a volume for the host/task def
        efs_volume = ecs.Volume(
            name="NginxConfigVolume",
            efs_volume_configuration=ecs.EfsVolumeConfiguration(
                file_system_id=file_system.file_system_id,
                # Ensure your EFS is set to use the correct root directory
                # root_directory="/path/to/nginx/configs" if your configs are not in the root
            ),
        )

        task_definition.add_volume(efs_volume)

        NEWSOLWEBAPP_cluster = self.cluster = ecs.Cluster(
            self,
            "NEWSOLWEBAPPCluster",
            cluster_name="NEWSOLWEBAPPCluster",
            vpc=vpc,
        )

        task_definition = ecs.FargateTaskDefinition(
            self,
            "NEWSOLWEBAPPTaskDefinition",
            cpu=512,
            memory_limit_mib=2048,
        )

        container = task_definition.add_container(
            "NEWSOLWEBAPPContainer",
            image=ecs.ContainerImage.from_registry("TODO"),
        )

        container.add_mount_points(
            ecs.MountPoint(
                container_path="/etc/nginx/nginx.conf",
                source_volume="NginxConfigVolume",
                read_only=True,
            ),
            ecs.MountPoint(
                container_path="/etc/nginx/conf.d",
                source_volume="NginxConfigVolume",
                read_only=True,
            ),
        )

        container.add_port_mappings(ecs.PortMapping(container_port=80))

        service = ecs.FargateService(
            self,
            "NEWSOLWEBAPPFargateService",
            cluster=NEWSOLWEBAPP_cluster,
            task_definition=task_definition,
            desired_count=2,
        )

        lb = elbv2.ApplicationLoadBalancer(self, "LB", vpc=vpc, internet_facing=True)

        listener = lb.add_listener("Listener", port=80)

        listener.add_targets("ECS", port=80, targets=[service])

    def read_env_file(self):
        env_vars = {}
        with open("../.prod.env", "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    secret = sm.Secret(
                        self,
                        f"{key}Secret",
                        secret_name=f"{self.stack_name}/{key}",
                        description=f"Secret for {key}",
                        generate_secret_string=sm.SecretStringGenerator(
                            secret_string_template=json.dumps({key: value}),
                            generate_string_key="dummy",
                        ),
                    )
                    env_vars[key] = ecs.Secret.from_secrets_manager(secret)
        return env_vars
