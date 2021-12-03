#
# This file is part of research-processing library
# Copyright (C) 2021 INPE.
#
# research-processing is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import docker


def _connect_to_docker_daemon() -> docker.DockerClient:
    """Connect to the docker daemon using the Docker environment variables.

    To connect to the Docker Daemon, this function uses the following environment variables:
     - `DOCKER_HOST`: The URL to the Docker host.
     - `DOCKER_TLS_VERIFY`: Verify the host against a CA certificate.
     - `DOCKER_CERT_PATH`: A path to a directory containing TLS certificates to use when connecting to the Docker host.

    Returns:
        docker.DockerClient: A client configured from environment variables.

    See:
        For more information about DockerClient and the information used to connect to the Docker Daemon, please
        refer to the Docker SDK for Python documentation: https://docker-py.readthedocs.io/en/stable/client.html
    """
    return docker.from_env(timeout=None)


class ContainerManager:
    """Docker Container Management.

    During the execution of the processing steps, Docker Containers are run with the necessary environments
    to use the processing tools (e.g., sen2cor, lasrc). The `ContainerManager` class manages which containers
    are running and which containers should be removed.

    When a `Docker Container` is run, the `ContainerManager` class keeps track of the logs generated by the `Container`
    and waits until the end of the operation before proceeding. In case of errors, the container that was being
    executed is terminated by the `ContainerManager`.
    """
    _running_containers = []

    @classmethod
    def remove_running_containers(cls):
        """Remove all running Docker Containers managed by `ContainerManager`."""
        for container in cls._running_containers:
            container.kill()

    @classmethod
    def run_container(cls, **kwargs):
        """Execute a container and follow the logs.

        Args:
            kwargs (Dict): Parameters to the `docker.DockerClient.containers.create` function.

        Returns:
            None: Container logs is presented on CLI.

        See:
            For more information about the `docker.DockerClient.containers.create` function, please refer to the
            Docker SDK for Python documentation: https://docker-py.readthedocs.io/en/stable/containers.html
        """
        client = _connect_to_docker_daemon()

        client.images.pull(kwargs["image"])
        container = client.containers.create(**kwargs)

        try:
            container.start()

            # if any problem is raised, then, register the container execution
            cls._running_containers.append(container)

            container.logs(follow=True)
        except:
            container.kill()
            raise

        cls._running_containers.remove(container)