import requests
import json

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"
STUDENT_ID = "23MH1A4416"
GITHUB_REPO_URL = "https://github.com/DuvvuLakshmiPrasanna/Task2_GPP"

# Read your public key
with open("student_public.pem", "r") as f:
    public_key = f.read()

payload = {
    "student_id": STUDENT_ID,
    "github_repo_url": GITHUB_REPO_URL,
    "public_key": public_key
}

headers = {"Content-Type": "application/json"}

print("Sending request to Instructor API...")
response = requests.post(API_URL, data=json.dumps(payload), headers=headers, timeout=20)

if response.status_code == 200:
    result = response.json()
    if "encrypted_seed" in result:
        encrypted_seed = result["encrypted_seed"]
        with open("encrypted_seed.txt", "w") as out:
            out.write(encrypted_seed)
        print("\n🎉 SUCCESS! Encrypted seed saved in encrypted_seed.txt")
    else:
        print("❌ Failed: Missing encrypted_seed in response")
        print(result)
else:
    print(f"❌ HTTP Error: {response.status_code}")
    print(response.text)
