#!/bin/bash
if [[ $TOKEN -eq "" ]]
then
	stop '$TOKEN not found. Run login.sh'
fi

curl -v \
	http://localhost:5000/complainers/complaints \
	-X GET \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer $TOKEN" \
	-d "{}"

