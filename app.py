from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_response():
    data = request.get_json()
    user_input = data.get("message", "")
    conversation_state = data.get("conversation_state", "initial")  # Get conversation state from frontend

    if conversation_state == "initial":
        # Step 1: Check if the user has specified either "sustainability" or "social impact"
        if "sustainability" in user_input.lower():
            follow_up_message = "Please provide more details about the sustainability goal you're aiming to achieve (e.g., reducing carbon emissions, waste management)."
            return jsonify({
                "response": follow_up_message,
                "conversation_state": "details",
                "user_option": "sustainability"
            })
        elif "social impact" in user_input.lower():
            follow_up_message = "Please provide more details about the social impact project you're focusing on (e.g., community education, health programs)."
            return jsonify({
                "response": follow_up_message,
                "conversation_state": "details",
                "user_option": "social impact"
            })
        else:
            return jsonify({
                "response": "Please specify if you're asking about 'sustainability' or 'social impact' to help me provide the right information.",
                "conversation_state": "initial"
            })
    
    elif conversation_state == "details":
        user_option = data.get("user_option")
        return generate_strategy(user_input, user_option)

    return jsonify({"error": "Invalid conversation state"}), 400

def generate_strategy(user_input, user_option):
    if user_option == "sustainability":
        prompt = (
            f"User is asking about sustainability. They provided the following details: {user_input}. "
            "Develop a strategic plan that includes measurable targets, actionable steps, and resources to achieve sustainability goals."
        )
    elif user_option == "social impact":
        prompt = (
            f"User is asking about social impact. They provided the following details: {user_input}. "
            "Develop a strategic plan that includes measurable targets, actionable steps, and resources to achieve social impact goals."
        )
    else:
        return jsonify({"error": "Invalid option provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ]
        )

        bot_reply = response['choices'][0]['message']['content']
        return jsonify({
            "response": bot_reply,
            "conversation_state": "complete"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)