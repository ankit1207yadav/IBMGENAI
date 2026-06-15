from flask import Flask, request, jsonify, render_template_string
from transformers import pipeline
import os

app = Flask(__name__)

# Load the generator model on startup
print("[LOADING] Loading model 'google/flan-t5-small'...")
try:
    generator = pipeline("text2text-generation", model="google/flan-t5-small")
    print("[SUCCESS] Model loaded successfully!")
except Exception as e:
    print(f"[ERROR] Error loading model: {e}")
    generator = None

# Emojis mapping
EMOJI_MAP = {
    "happy": "😊",
    "tired": "😴",
    "anxious": "😟",
    "angry": "😠",
    "excited": "🤩",
    "sad": "😢",
    "neutral": "🙂"
}

# Serve the HTML page directly using render_template_string for single-file deployment
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InspireMe AI - Watsonx GenAI Demo</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: rgba(20, 30, 55, 0.65);
            --border-color: rgba(255, 255, 255, 0.08);
            --text-primary: #ffffff;
            --text-secondary: #a0aec0;
            --accent-primary: #3b82f6;
            --accent-secondary: #8b5cf6;
            --success-color: #10b981;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-primary);
            font-family: 'Outfit', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 40%);
        }

        .container {
            width: 100%;
            max-width: 600px;
            background: var(--card-bg);
            backdrop-filter: blur(16px) saturate(180%);
            -webkit-backdrop-filter: blur(16px) saturate(180%);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
            position: relative;
            z-index: 10;
        }

        header {
            text-align: center;
            margin-bottom: 30px;
        }

        .logo-badge {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: white;
            font-size: 0.85rem;
            font-weight: 600;
            padding: 6px 16px;
            border-radius: 50px;
            display: inline-block;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }

        h1 {
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 10px;
            background: linear-gradient(to right, #ffffff, #a5b4fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 1rem;
            line-height: 1.5;
        }

        .form-group {
            margin-bottom: 25px;
        }

        .label {
            display: block;
            margin-bottom: 12px;
            font-weight: 600;
            color: var(--text-primary);
            font-size: 0.95rem;
        }

        .mood-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 15px;
        }

        .mood-btn {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 12px 10px;
            color: var(--text-primary);
            font-family: inherit;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
        }

        .mood-btn:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: var(--accent-primary);
            transform: translateY(-2px);
        }

        .mood-btn.active {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.2));
            border-color: var(--accent-primary);
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.15);
        }

        .mood-btn .emoji {
            font-size: 1.5rem;
        }

        .input-custom {
            width: 100%;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 14px;
            color: white;
            font-family: inherit;
            font-size: 1rem;
            transition: all 0.2s ease;
            outline: none;
        }

        .input-custom:focus {
            border-color: var(--accent-primary);
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.15);
        }

        .submit-btn {
            width: 100%;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: white;
            border: none;
            border-radius: 12px;
            padding: 16px;
            font-size: 1.1rem;
            font-weight: 600;
            font-family: inherit;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.25);
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 24px rgba(59, 130, 246, 0.35);
            filter: brightness(1.1);
        }

        .submit-btn:active {
            transform: translateY(1px);
        }

        .submit-btn:disabled {
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-secondary);
            cursor: not-allowed;
            box-shadow: none;
            transform: none;
        }

        .spinner {
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-top: 2px solid white;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            display: none;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .result-card {
            margin-top: 30px;
            border: 1px solid var(--border-color);
            background: rgba(0, 0, 0, 0.15);
            border-radius: 16px;
            padding: 24px;
            display: none;
            animation: fadeIn 0.4s ease forwards;
            position: relative;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .result-card::before {
            content: "“";
            position: absolute;
            top: 10px;
            left: 20px;
            font-size: 4rem;
            font-family: serif;
            color: rgba(255, 255, 255, 0.05);
            line-height: 1;
        }

        .result-title {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: var(--accent-primary);
            margin-bottom: 10px;
            font-weight: 600;
        }

        .result-text {
            font-size: 1.2rem;
            line-height: 1.6;
            color: var(--text-primary);
            font-style: italic;
        }

        .course-footer {
            margin-top: 35px;
            text-align: center;
            border-top: 1px solid var(--border-color);
            padding-top: 25px;
            font-size: 0.8rem;
            color: var(--text-secondary);
            line-height: 1.6;
        }

        .course-footer strong {
            color: var(--text-primary);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo-badge" id="logoBadge">Watsonx GenAI</div>
            <h1 id="mainTitle">InspireMe AI</h1>
            <p class="subtitle" id="mainSubtitle">Get personalized motivational quotes powered by Google's FLAN-T5 model</p>
        </header>

        <div class="form-group">
            <span class="label">Select your mood:</span>
            <div class="mood-grid" id="moodGrid">
                <button type="button" class="mood-btn" data-mood="happy" id="btnHappy">
                    <span class="emoji">😊</span>
                    <span>Happy</span>
                </button>
                <button type="button" class="mood-btn" data-mood="sad" id="btnSad">
                    <span class="emoji">😢</span>
                    <span>Sad</span>
                </button>
                <button type="button" class="mood-btn" data-mood="tired" id="btnTired">
                    <span class="emoji">😴</span>
                    <span>Tired</span>
                </button>
                <button type="button" class="mood-btn" data-mood="anxious" id="btnAnxious">
                    <span class="emoji">😟</span>
                    <span>Anxious</span>
                </button>
                <button type="button" class="mood-btn" data-mood="angry" id="btnAngry">
                    <span class="emoji">😠</span>
                    <span>Angry</span>
                </button>
                <button type="button" class="mood-btn" data-mood="excited" id="btnExcited">
                    <span class="emoji">🤩</span>
                    <span>Excited</span>
                </button>
            </div>
            
            <input type="text" class="input-custom" id="customMoodInput" placeholder="Or type any other mood (e.g., confused, calm)...">
        </div>

        <button class="submit-btn" id="generateButton">
            <span class="spinner" id="btnSpinner"></span>
            <span id="btnText">✨ Generate Motivation</span>
        </button>

        <div class="result-card" id="resultCard">
            <div class="result-title" id="resultTitle">💡 Inspiration for you</div>
            <div class="result-text" id="resultText">Motivational message will appear here...</div>
        </div>

        <div class="course-footer" id="courseFooter">
            Developed during <strong>Generative AI using IBM Watsonx</strong> course<br>
            <strong>IBM Career Education Program</strong> in collaboration with <strong>VIT</strong>
        </div>
    </div>

    <script>
        const moodButtons = document.querySelectorAll('.mood-btn');
        const customMoodInput = document.getElementById('customMoodInput');
        const generateBtn = document.getElementById('generateButton');
        const btnSpinner = document.getElementById('btnSpinner');
        const btnText = document.getElementById('btnText');
        const resultCard = document.getElementById('resultCard');
        const resultText = document.getElementById('resultText');
        const resultTitle = document.getElementById('resultTitle');

        let selectedMood = '';

        // Select mood from buttons
        moodButtons.forEach(button => {
            button.addEventListener('click', () => {
                moodButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                selectedMood = button.getAttribute('data-mood');
                customMoodInput.value = ''; // clear custom input
            });
        });

        // Clear button active state when custom text is entered
        customMoodInput.addEventListener('input', () => {
            if (customMoodInput.value.trim() !== '') {
                moodButtons.forEach(btn => btn.classList.remove('active'));
                selectedMood = customMoodInput.value.trim();
            }
        });

        // Trigger generate logic
        generateBtn.addEventListener('click', async () => {
            let mood = selectedMood;
            if (customMoodInput.value.trim() !== '') {
                mood = customMoodInput.value.trim();
            }

            if (!mood) {
                alert('Please select or enter a mood first!');
                return;
            }

            // Set loading state
            generateBtn.disabled = true;
            btnSpinner.style.display = 'block';
            btnText.innerText = 'Consulting Watsonx LLM...';
            resultCard.style.display = 'none';

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ mood: mood })
                });
                
                const data = await response.json();
                
                if (data.quote) {
                    resultText.innerText = data.quote;
                    resultTitle.innerText = `💡 Inspiration for feeling ${mood} ${data.emoji || ''}`;
                    resultCard.style.display = 'block';
                } else {
                    resultText.innerText = "Error: " + (data.error || "Failed to generate motivation.");
                    resultCard.style.display = 'block';
                }
            } catch (error) {
                resultText.innerText = "Error communicating with backend.";
                resultCard.style.display = 'block';
            } finally {
                // Reset button state
                generateBtn.disabled = false;
                btnSpinner.style.display = 'none';
                btnText.innerText = '✨ Generate Motivation';
            }
        });
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(INDEX_HTML)

@app.route("/generate", methods=["POST"])
def generate():
    if not generator:
        return jsonify({"error": "Model not loaded on server."}), 500
        
    data = request.json or {}
    mood = data.get("mood", "").strip().lower()
    
    if not mood:
        return jsonify({"error": "Mood parameter is required"}), 400

    emoji = EMOJI_MAP.get(mood, "🧘")
    
    # Run the generation pipeline
    prompt = f"Give me a short motivational quote for someone who is feeling {mood}."
    try:
        response = generator(prompt, max_length=50, do_sample=True, temperature=0.8)
        generated_text = response[0]['generated_text']
        
        # Clean up any leading symbols or whitespaces from the generated output
        generated_text = generated_text.strip().lstrip("✨").lstrip("“").lstrip('"').rstrip("”").rstrip('"').strip()
        
        # Fallback if generation is empty
        if not generated_text:
            generated_text = "Keep moving forward! Great things take time."
            
        return jsonify({
            "mood": mood,
            "emoji": emoji,
            "quote": generated_text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
