#!/bin/bash
curl -v \
	http://localhost:5000/login/ \
	-X POST \
	-H "Content-Type: application/json" \
	-d '{"email": "test@example.com", "password": "1234Aa!11111"}'

