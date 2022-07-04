#!/bin/bash
curl \
	localhost:5000/books/ \
	-H 'Content-Type: application/json' \
	-X POST \
	-d '{"author": "test", "title": "test"}'

