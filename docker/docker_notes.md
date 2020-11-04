# Docker notes

## WSL Connect to Docker deamon
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```
docker -H localhost:2375 images
export DOCKER_HOST=localhost:2375
```

## SSH into a running container
```
docker ps
docker exec -it <container ID> /bin/bash
```

## Execute a command in Docker container
```
docker exec -it <container name> <command>
```