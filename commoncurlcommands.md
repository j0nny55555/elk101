Curl Commands:
==========================================

curl -XGET 'localhost:9200/_tasks?pretty'
curl -XGET 'localhost:9200/_tasks?actions=cluster:*&pretty'
curl -XGET 'localhost:9200/_tasks?nodes=nodeId1,nodeId2&pretty'
curl -XGET 'localhost:9200/_tasks?nodes=nodeId1,nodeId2&actions=cluster:*&pretty'

curl -XGET 'localhost:9200/_cluster/health?pretty'
curl -XGET 'localhost:9200/_cluster/pending_tasks?pretty'

curl -XGET 'localhost:9200/_all/_stats?pretty'

curl -XGET 'localhost:9200/_nodes/stats?pretty'

GET _nodes/stats

Kibana Debugger Commands:
=========================================

POST indexname/_delete_by_query?conflicts=proceed
{
  "query": {
    "match_all": {
    }
  }
}

GET /_cat/indices/*?v&s=index

GET _all/_stats

GET _cluster/health

GET _nodes/stats

GET _tasks

GET _tasks?actions=cluster:*

POST indexname.*/_delete_by_query?conflicts=proceed
{
  "query": {
      "exists": {
        "field": "fieldname.keyword"
      }
  }
}

DELETE indexname