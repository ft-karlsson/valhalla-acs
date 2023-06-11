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
- [ ] create kafka topics if not present
- [ ] add docker/podman build
- [ ] topology graph persisted in kafka
- [ ] build policy/rules engine prototype

