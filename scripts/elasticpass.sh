#!/bin/bash
curl -XPOST 'elastic:changeme@localhost:9200/_xpack/security/user/elastic/_password?pretty' -H 'Content-Type: application/json' -d'
{
  "password": "yournewpassword"
}
'
