#!/bin/bash
curl \
	localhost:5000/readers/ \
	-H 'Content-Type: application/json' \
	-X POST \
	-d '{"first_name": "test", "last_name": "test"}'

