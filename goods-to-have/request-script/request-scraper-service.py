import time
import requests
import sys

headers = {"Content-Type": "application/json"}
url = "http://localhost:8080"

print("The file used is %s" %sys.argv[1])
print("The time between requests is %s seconds" %sys.argv[2])
print("Starting Request Script")
try:
    with open(sys.argv[1], "r") as file:
        for line in file:
            payload = '{"url": "'+ line.rstrip() + '"}'
            print("Request to  %s" %line)
            response = requests.post(url, data=payload, headers=headers)
            time.sleep(int(sys.argv[2]))
except KeyboardInterrupt:
    print("Shutting down...")
