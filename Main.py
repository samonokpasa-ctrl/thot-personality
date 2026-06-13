import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

PUTER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InYyIn0.eyJ0IjoidCIsInYiOiIyIiwidG9rZW5fdWlkIjoiYzc4MDY2ZGMtYTY5Mi00YWUwLWE4ZDUtMjE2YWRiYjJmYjlhIiwidXUiOiJ6RysvQld3VFRocUZlU2ZZS0MxdTNRPT0iLCJzdSI6IkNVZ2lNdUVMVGppdFVpb2lrZ2s2eVE9PSIsImFpIjoiekcrL0JXd1RUaHFGZVNmWUtDMXUzUT09IiwiZnVsbF9hY2Nlc3MiOnRydWUsImlhdCI6MTc4MTI2Nzk3OX0.lyr4y1FhPvN-vhQbWUB_SFunyz_y-hY4ZbZKDLVpouI"

@app.route('/')
def home():
    return "THOT Personality Server is running! 🚀"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('message', '')
    
    if not question:
        return jsonify({"error": "No message"}), 400
    
    personality = f"""You are THOT, Sam's personal AI assistant.
Rules:
- Be casual, friendly, use emojis 😊😏
- Keep replies UNDER 80 words
- Call Sam by name
- NEVER list your capabilities
- Just answer directly like a friend

Sam asked: "{question}"

Your short response as THOT:"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PUTER_TOKEN}"
    }
    
    response = requests.post(
        "https://api.puter.com/puterai/openai/v1/chat/completions",
        headers=headers,
        json={
            "model": "gpt-5-nano",
            "messages": [{"role": "user", "content": personality}]
        },
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        answer = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        return jsonify({"response": answer})
    else:
        return jsonify({"error": "AI error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
