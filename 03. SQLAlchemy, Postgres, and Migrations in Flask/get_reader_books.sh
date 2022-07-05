#!/bin/bash
curl \
	localhost:5000/readers/1/books/ \
	-H 'Content-Type: application/json' \
	-X GET

