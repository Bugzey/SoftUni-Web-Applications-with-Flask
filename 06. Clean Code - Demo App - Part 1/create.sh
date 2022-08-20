#!/bin/bash
if [[ $TOKEN -eq "" ]]
then
	stop '$TOKEN not found. Run login.sh'
fi

curl -v \
	http://localhost:5000/complainers/complaints \
	-X POST \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer $TOKEN" \
	-d '{"title": "test 1", "description": "some complaint", "photo_url": "https://example.com/picture", "amount": 9000.0}'

