---
layout: default
nav_order: 0
title: Home
---

# Disaster Risk Observability Pipeline v{{ site.drop_version }}

## Introduction

Disaster Risk Observability Pipeline (DROP) is a data processing pipeline to 
predict the type, severity, and geo location of disasters events worldwide.

## System Design

The pipeline leverages event-driven, and microservice architectures, and 
multilingual NER models to crawl, predict, and geocode historical, and
realtime events at scale.

Events are fetched from external sources and fed by
[topic]({{ site.baseurl }}/glossary#topic) into the event log.

From there, various data transformation steps consume the events, perform some
transformation, and feed the transformed events back to the event log,
to be consumed by the next steps.

![System Design]({{ site.baseurl }}/images/design.png)

## What's Next?

Let us [get started]({{ site.baseurl }}/get_started).
