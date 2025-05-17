import requests

data = {"features": [5.1, 3.5, 1.4, 0.2]}
response = requests.post("http://localhost:5000/predict", json=data)

print("Status code:", response.status_code)
print("Response text:", response.text)

try:
    print("JSON response:", response.json())
except Exception as e:
    print("Failed to parse JSON:", e)

#testing with curl
#Invoke-RestMethod -Uri http://localhost:5000/predict -Method Post -Body (@{features = @(5.1, 3.5, 1.4, 0.2)} | ConvertTo-Json) -ContentType "application/json"
