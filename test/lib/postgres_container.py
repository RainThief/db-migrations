"""postgres container module"""


from test.lib.database import DatabaseConnection
import docker as dockerlib
from robot_support.docker import Container


CONTAINER_NAME = "robot-postgres"

docker = Container(CONTAINER_NAME)


def start(db_image: str, capture_log: bool = False):
    """Start postgres container

    Args:
        **capture_log: capture docker logs (requires DEBUG log level)
    """

    docker.run(
        db_image,
        detach=True,
        name="robot-postgres",
        remove=True,
        log=capture_log,
        environment={
            'POSTGRES_USER': 'user',
            'POSTGRES_DB': 'db',
            'POSTGRES_PASSWORD': 'password'
        },
        ports={
            '5432/tcp': 5432
        },
        readycheck=(DatabaseConnection.SQLDatabase.connect, [])
    )


def stop():
    """stop postgres container"""
    try:
        docker.stop()
    except dockerlib.errors.NotFound:
        pass
