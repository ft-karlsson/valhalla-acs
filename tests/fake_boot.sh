#!/bin/sh
# this will mock a request using xml example
curl http://127.0.0.1:8000/deviceapi --data-binary "@tests/invalid_soap_inform.txt"
