# valhalla-acs


## Kafka as persistence


## running locally
prerequisite: python 3.11.3 or higher


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
- [x] shellscript to mimick device inform message
- [x] build device_api() as receiver
- [ ] dynamic graph from kafka/topology
- [ ] build policy/rules engine prototype


### nice to have:
- [ ] try to use custom decorator
- [ ] add kafka setup 
- [ ] create kafka topics if not present
- [ ] fix logging instead of prints
- [ ] add docker/podman build
- [ ] add docker podman compose build

