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
python -m unittest discover -s tests -p "test_*.py"


## TODO:
### need to have: 
- [x] add datamodel
- [x] add frontend
- [x] add async main
- [ ] dynamic graph from kafka/topology
- [ ] build device_api() as receiver
- [ ] build policy/rules engine prototype
- [ ] shellscript to mimick device inform message

### nice to have:
- [ ] add kafka setup 
- [ ] fix logging instead of prints
- [ ] add docker/podman build
- [ ] add docker podman compose build
- [ ] unittest
