import pulumi
import pulumi_kubernetes as kubernetes

config = pulumi.Config()

name = config.require("name")
image = config.require("image")
container_port = config.require_int("container_port")

app_labels = {
    "app.kubernetes.io/name": name,
}

metadata=kubernetes.meta.v1.ObjectMetaArgs(
    labels=app_labels,
    name=name,
    namespace=name,
)
 
namespce = kubernetes.core.v1.Namespace(
    name,
    metadata=metadata
)

deployment = kubernetes.apps.v1.Deployment(
    name,
    metadata=metadata,
    spec=kubernetes.apps.v1.DeploymentSpecArgs(
        selector=kubernetes.meta.v1.LabelSelectorArgs(match_labels=app_labels),
        replicas=2,
        template=kubernetes.core.v1.PodTemplateSpecArgs(
            metadata=kubernetes.meta.v1.ObjectMetaArgs(labels=app_labels),
            spec=kubernetes.core.v1.PodSpecArgs(
                containers=[
                    kubernetes.core.v1.ContainerArgs(
                        name=name, 
                        image=image,
                        ports=[
                            kubernetes.core.v1.ContainerPortArgs(
                                name="http",
                                container_port=container_port,
                            ),
                        ],
                    )
                ]
            )
        ),
    )
)

service = kubernetes.core.v1.Service(
    name, 
    metadata=metadata,
    spec=kubernetes.core.v1.ServiceSpecArgs(
        selector=app_labels,
        type="NodePort",
        ports=[
            kubernetes.core.v1.ServicePortArgs(
                name="http",
                protocol="TCP",
                port=80,
                target_port="http",
            )
        ],
    )
)

ingress = kubernetes.networking.v1.Ingress(
    name,
    metadata=metadata,
    spec=kubernetes.networking.v1.IngressSpecArgs(
        rules=[
            kubernetes.networking.v1.IngressRuleArgs(
                http=kubernetes.networking.v1.HTTPIngressRuleValueArgs(
                    paths=[
                        kubernetes.networking.v1.HTTPIngressPathArgs(
                            backend=kubernetes.networking.v1.IngressBackendArgs(
                                service=kubernetes.networking.v1.IngressServiceBackendArgs(
                                    name=name,
                                    port=kubernetes.networking.v1.ServiceBackendPortArgs(
                                        name="http",
                                    ),
                                ),
                            ),
                            path="/",
                            path_type="Prefix",
                        )
                    ],
                ),
            )
        ],
    )
)
