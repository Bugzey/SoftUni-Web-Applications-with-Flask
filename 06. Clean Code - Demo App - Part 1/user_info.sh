#!/bin/bash
curl -v \
	http://localhost:5000/users/ \
	-X GET \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer $TOKEN" \

