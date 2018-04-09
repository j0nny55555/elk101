Logstash takes quite a bit of tunning, in that here are some helpful commands
====================================================================
Put Logstash into a standard out mode, it will literally show you all rubydebug
```shell
/usr/share/logstash/bin/logstash -f /etc/logstash/conf.d/pipelinename.conf --config.reload.automatic
```
Watch the Logstash service and other bits for errors
```shell
sudo tail -f -n20 /usr/share/logstash/logs/logstash-plain.log
sudo tail -f -n30 /var/log/logstash/logstash-plain.log
tail -f /tmp/metrics.log
tail -f /tmp/errors.log
```
Fire off the Filebeat log send
```shell
/usr/share/filebeat/bin/filebeat -e -c /etc/filebeat/filebeat.yml -path.home /usr/share/filebeat -path.config /etc/filebeat -path.data /var/log/filebeat -d "pubish" -once
```
Clean up after a bad send
```shell
rm /tmp/metrics.log
rm /tmp/errors.log
rm /var/log/filebeat/registry
```