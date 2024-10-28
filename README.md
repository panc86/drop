# Disaster Risk Observability Pipeline (DROP)

Disaster Risk Observability Pipeline (DROP) is a data processing pipeline 
to predict the type, severity, and geo location of disasters events worldwide.

It leverages event-driven, and microservice architectures, and multilingual NER 
models to crawl, predict, and geocode historical, and realtime events at scale.

## Prerequisites

- Linux OS
- 8G RAM
- 8 CPUs
- Python ~3.10
- Docker Engine

## Build

```shell
bash ./pipeline/build.sh
```

## Deploy

Single node deployment

```shell
export KAFKA_BROKER_HOST=<hostname/ip>
docker compose up
```

Multi node deployment

```shell
export KAFKA_BROKER_HOST=<hostname/ip>
docker stack deploy --detach=false -c compose.yaml -c compose.swarm.yaml drop
```

> More than 1 node running Docker in Swarm mode is required to run this deployment.
> For more info, read the [Docker Documentation](https://docs.docker.com/engine/swarm/).
