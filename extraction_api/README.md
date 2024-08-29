# Extraction API

## Build index with mapping

It is recommended to set a strict mapping for production Elasticsearch indices

```http
PUT extractions
{
  "mappings": {
    "properties": {
      "begin": {
        "type": "date"
      },
      "created_at": {
        "type": "date"
      },
      "end": {
        "type": "date"
      },
      "executed": {
        "type": "boolean"
      },
      "id": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "keywords": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "tag": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      }
    }
  }
}
```
