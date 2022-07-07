#!/bin/bash
curl -v \
	http://localhost:5000/users/ \
	-X POST \
	-H "Content-Type: application/json" \
	-d '{"username": "test", "password": "1234Aa!"}'

