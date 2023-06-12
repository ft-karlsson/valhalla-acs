# new-acs (Working title: Valhalla ACS)
Highly scalable and modular kafka-based ACS system built for cloud.

## Kafka as persistence / before starting ACS server
install kafka: https://developer.confluent.io/faq/apache-kafka/install-and-run/#install-and-run-how-to-install-kafka

depending on your client - you can create the topics with following settings: 

creating the topics: 
```shell 
kafka-topics --bootstrap-server localhost:9092 --create --topic acs_devices --replication-factor 1 --partitions 1 --config "cleanup.policy=compact" --config "delete.retention.ms=1209600000"  --config "segment.ms=50400000" --config "min.cleanable.dirty.ratio=0.01"
```


```shell 
kafka-topics --bootstrap-server localhost:9092 --create --topic acs_subscribers --replication-factor 1 --partitions 1 --config "cleanup.policy=compact" --config "delete.retention.ms=1209600000"  --config "segment.ms=50400000" --config "min.cleanable.dirty.ratio=0.01"
```

```shell 
kafka-topics --bootstrap-server localhost:9092 --create --topic acs_device_policies --replication-factor 1 --partitions 1 --config "cleanup.policy=compact" --config "delete.retention.ms=1209600000"  --config "segment.ms=50400000" --config "min.cleanable.dirty.ratio=0.01"
```


Then you can produce to topics with messages like this (prompt):
```shell
kafka-console-producer --topic acs_subscribers --bootstrap-server localhost:9092 --property "parse.key=true" --property "key.separator=/"
````

```shell
>su0112330/{"devices":[{"serialnumber":"SE1936018000231"}],"first_name":"Frederik","last_name":"Karlsson","products":[{"product_id":11}],"subscriber_id":"su0112330","type":"consumer"}
```




## running locally
prerequisite: python 3.11.3 or higher
prerequisite: running kafka - see kafka as persistence



### create virtual env so not to disturb system python
```shell
python3 -m venv venv
```

```shell
source venv/bin/activate
```

### install dependencies
```shell
pip install -r requirements.txt
```

### start the application using uvicorn as http server
```shell
uvicorn main:app --reload --log-level debug --port 8000
```

### note on graphviz:
Installation may vary on OS - see docs for detailed instructions: https://pygraphviz.github.io/documentation/stable/install.html


### run unittests
```shell 
python -m unittest discover -s tests -p "test_*.py"
```


### mock boot events from devices
```shell
sh ./tests/mock_boot_event.sh
```

## TODO:
### need to have: 
- [x] unittest
- [x] add datamodel
- [x] add frontend
- [x] add async main
- [x] add soap_parser
- [x] add topology graph
- [x] shellscript to mimick device inform message
- [x] build device_api() as receiver
- [x] use build pattern for datamodel
- [x] build datamodel validator class / decorator
- [x] add protype search module for devices using subscriber key




### nice to have:
- [x] try to use custom decorator
- [ ] fix logging instead of prints
- [ ] add docker podman compose build
- [ ] add kafka setup 
- [ ] create kafka topics on startup if not present
- [ ] add docker/podman build
- [ ] topology graph persisted in kafka
- [ ] build policy/rules engine prototype

