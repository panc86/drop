---
layout: default
nav_order: 1
title: Get Started
---

# Get Started

## Prerequisites

The following applications should be installed on your machine:
- Python ~3.10
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Swarm mode](https://docs.docker.com/engine/swarm/swarm-tutorial/)
- 3 node cluster.

{: .warning}
Traffic on the following ports must be enable a Docker Swarm master node to
communicate with other nodes in the cluster:
2376/tcp, 2377/tcp, 7946/tcp, 7946/udp, 4789/udp, 80/tcp

## Get Source Code

Clone the [source code](https://github.com/panc86/drop.git).

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
