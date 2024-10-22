---
layout: default
nav_order: 0
parent: Pipelines
title: Text Pipeline
---

# Text Pipeline
{:.no_toc}

Text processing pipeline is made of the following steps

1. TOC
{:toc}

## Annotators

Annotate batches of pre-processed multilingual texts with an array of probabilities
using binary models trained on natural disasters related texts.

Feature Extraction operations:
* extract required 
* normalize URLs
* normalize hashtags
* remove punctuation
* normalize white spaces
* remove new lines
* remove dates
* merge neighbouring word duplicates

Available annotators:
* [Flood](https://zenodo.org/record/6351658)
* [Impact](https://zenodo.org/record/6577394)

## Geocoder

Matches geographic locations identified from texts using DeepPavlov 
Named Entity Recognizer (NER) against a given gazetteer.
