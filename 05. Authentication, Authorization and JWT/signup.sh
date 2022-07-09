#!/bin/bash
curl -v \
	http://localhost:5000/signup/ \
	-X POST \
	-H "Content-Type: application/json" \
	-d '{"username": "test", "email": "test@example.com", "password": "1234Aa!11111", "first_name": "test", "last_name": "test"}'

