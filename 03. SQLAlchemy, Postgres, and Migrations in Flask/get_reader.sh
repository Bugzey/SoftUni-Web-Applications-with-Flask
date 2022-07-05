#!/bin/bash
curl \
	localhost:5000/readers/1/ \
	-H 'Content-Type: application/json' \
	-X GET

