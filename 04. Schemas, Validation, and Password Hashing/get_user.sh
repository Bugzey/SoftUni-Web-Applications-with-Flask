#!/bin/bash
curl \
	localhost:5000/user/1/ \
	-H 'Content-Type: application/json' \
	-X GET

