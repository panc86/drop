# Disaster Risk Observability Pipeline (DROP)

Disaster Risk Observability Pipeline (DROP) is a data processing pipeline 
to predict the type, severity, and geo location of disasters events worldwide.

It leverages event-driven, and microservice architectures, and multilingual NER 
models to crawl, predict, and geocode historical, and realtime events at scale.

## Requirements

- Linux OS
- 8G RAM
- 8 CPUs
- Python ~3.10
- Docker Engine

## Build

Build pipeline steps

```shell
bash ./pipeline/build.sh
```

## Deploy

Single node

```shell
docker compose up
```

Multi node

```shell
docker stack deploy --detach=false -c compose.yaml -c compose.placement.yaml drop
```

> For more info on Docker Swarm, read the [Docker Documentation](https://docs.docker.com/engine/swarm/).
