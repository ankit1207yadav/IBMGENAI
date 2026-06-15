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

import random

QUOTE_DATABASE = {
    "happy": [
        "Happiness is not something ready-made. It comes from your own actions.",
        "Enjoy the little things, for one day you may look back and realize they were the big things.",
        "The most wasted of all days is one without laughter.",
        "Be happy for this moment. This moment is your life.",
        "Happiness is a warm glow that starts from within and spreads to others."
    ],
    "sad": [
        "It's okay to have bad days. The clouds will clear, and the sun will shine again.",
        "Difficult roads often lead to beautiful destinations.",
        "You are stronger than you think, and this too shall pass.",
        "Every storm runs out of rain. Stay strong, brighter days are coming.",
        "The stars need darkness to shine. Keep holding on."
    ],
    "tired": [
        "Rest if you must, but don't quit. You are doing great.",
        "It is okay to pause and recharge. Your dreams will wait for you.",
        "Even the strongest need rest to shine bright again. Take it easy.",
        "Tired minds need rest, not quit. Recharge and start fresh tomorrow.",
        "Give yourself permission to rest. You've been working hard."
    ],
    "anxious": [
        "Breathe. You have survived 100% of your hardest days so far. You've got this.",
        "Do not let the shadows of tomorrow darken the light of today.",
        "Take it one breath, one step, one moment at a time. You are safe.",
        "Trust the process. You are stronger than your worries.",
        "Quiet the mind, quiet the soul. You are doing the best you can."
    ],
    "angry": [
        "Control your anger; it is only one letter short of danger. Stay calm and rise above.",
        "Do not let the storm in your mind steal the peace in your heart.",
        "Your peace of mind is worth more than winning an argument.",
        "In the middle of a storm, peace is your superpower. Breathe out the anger.",
        "Speak when you are angry and you will make the best speech you will ever regret."
    ],
    "excited": [
        "Let your passion fly! This excitement is the fuel for your next big achievement.",
        "Capture this beautiful energy and run towards your dreams!",
        "Your enthusiasm is contagious—let it light up the world!",
        "Believe in your energy. You are on the verge of something incredible.",
        "Keep that wonderful energy going and inspire everyone around you."
    ],
    "general": [
        "Keep moving forward. Great things take time and patience.",
        "Believe you can and you're halfway there.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Act as if what you do makes a difference. It does.",
        "The only way to do great work is to love what you do."
    ]
}

def get_mood_category(mood_str):
    mood_str = mood_str.lower().strip()
    if mood_str in QUOTE_DATABASE:
        return mood_str
        
    mappings = {
        "happy": ["joy", "glad", "cheerful", "delighted", "good", "great", "awesome", "blessed", "content"],
        "sad": ["down", "blue", "depressed", "heartbroken", "lonely", "grief", "hopeless", "hurt", "crying"],
        "tired": ["exhausted", "sleepy", "drained", "weak", "fatigued", "lazy", "burnt", "burnout"],
        "anxious": ["nervous", "stressed", "worried", "scared", "fear", "panic", "overwhelmed", "tense"],
        "angry": ["mad", "furious", "annoyed", "frustrated", "irritated", "hate", "rage"],
        "excited": ["thrilled", "eager", "hyped", "energetic", "passion", "pumped"]
    }
    
    for category, keywords in mappings.items():
        if mood_str in keywords:
            return category
        for kw in keywords:
            if kw in mood_str:
                return category
                
    return "general"

@app.route("/generate", methods=["POST"])
def generate():
    if not generator:
        return jsonify({"error": "Model not loaded on server."}), 500
        
    data = request.json or {}
    mood = data.get("mood", "").strip().lower()
    
    if not mood:
        return jsonify({"error": "Mood parameter is required"}), 400

    emoji = EMOJI_MAP.get(mood, "🧘")
    
    # 1. Retrieve a high-quality base quote matching the mood
    category = get_mood_category(mood)
    base_quotes = QUOTE_DATABASE[category]
    base_quote = random.choice(base_quotes)
    
    # 2. Use google/flan-t5-small to dynamically paraphrase and customize the quote
    prompt = f"Paraphrase this motivational quote: {base_quote}"
    try:
        response = generator(prompt, max_new_tokens=60, do_sample=True, temperature=0.7, repetition_penalty=1.2)
        generated_text = response[0]['generated_text']
        
        # Clean up any leading symbols or quotes
        generated_text = generated_text.strip().lstrip("✨").lstrip("“").lstrip('"').rstrip("”").rstrip('"').strip()
        
        # Make sure the generated sentence starts with a capital letter
        if generated_text:
            generated_text = generated_text[0].upper() + generated_text[1:]
            
        # Fallback to the beautiful base quote if generation is empty or too short
        if not generated_text or len(generated_text) < 15:
            generated_text = base_quote
            
        return jsonify({
            "mood": mood,
            "emoji": emoji,
            "quote": generated_text
        })
    except Exception as e:
        # Graceful fallback to the high-quality base quote on model failure
        return jsonify({
            "mood": mood,
            "emoji": emoji,
            "quote": base_quote,
            "warning": f"Model fallback activated: {str(e)}"
        })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
