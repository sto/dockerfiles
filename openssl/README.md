# Docker image to run openssl on a container

## Info

Idea taken from https://github.com/ellerbrock/openssl-docker

## Build

```shell
docker build -t stodh/openssl .
```

## Push

```shell
docker push stodh/openssl
```

## Run

* Interactive openssl execution:

```shell
docker run -it --rm -u "$(id -u):$(id -g)" -v "$(pwd):/ssl" -w "/ssl"
```

* Certificate generation:

```shell
docker run -it --rm -u "$(id -u):$(id -g)" -v "$(pwd):/ssl" -w "/ssl" \
	   stodh/openssl req -x509 -nodes -new -newkey rsa:4096 -days 365 \
	                     -keyout "/ssl/key.pem" -out "/ssl/cert.pem";
```
