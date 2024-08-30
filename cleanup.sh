#!/bin/bash

# Run the curl command to trigger the cleanup
curl --location --request POST 'https://fastapi-production-a6ed.up.railway.app/cleanup'
