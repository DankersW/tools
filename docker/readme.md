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

## Connect to a remote Docker daemon with this 1 liner:
```
echo "export DOCKER_HOST=tcp://localhost:2375" >> ~/.bashrc && source ~/.bashrc
```

## Execute a command in Docker container
```
docker exec -it <container name> <command>
```

Start a shell inside a new container
```sh
docker run --rm -it --entrypoint /bin/bash <image_name>
```

## Docker push
Push image to docker hub
```
docker login -u dankersw
docker tag docker_image:latest dankersw/docker_repo:tag
docker push dankersw/docker_repo:tag
```
