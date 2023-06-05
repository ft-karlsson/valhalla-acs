# valhalla-acs


## Kafka as persistence

## running locally
```python3 -m venv venv```

### create virtual env so not to disturb system python
```source source/bin/activate```

### install dependencies
```pip install -r requirements.txt```

### start the application using uvicorn as http server
```uvicorn main:app --reload --log-level debug --port 8000```

### note on graphviz:
Installation may vary on os - see docs for detailed instructions: https://pygraphviz.github.io/documentation/stable/install.html





## TODO:
### need to have: 
- [x] add datamodel
- [x] add frontend
- [x] add async main
- [ ] dynamic graph from kafka/topology
- [ ] build device_api() as receiver
- [ ] build policy/rules engine prototype

### nice to have:
- [ ] add kafka setup 
- [ ] fix logging instead of prints
- [ ] add docker/podman build
- [ ] add docker podman compose build
