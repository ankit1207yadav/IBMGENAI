# 🌟 InspireMe AI (IBM Watsonx GenAI Project)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A5%97-Hugging%20Face-yellow.svg?style=for-the-badge)](https://huggingface.co/)
[![IBM Watsonx](https://img.shields.io/badge/IBM-Watsonx-blue.svg?style=for-the-badge&logo=ibm&logoColor=white)](https://www.ibm.com/watsonx)
[![VIT](https://img.shields.io/badge/VIT-Collaboration-red.svg?style=for-the-badge)](https://vit.ac.in/)

Welcome to **InspireMe AI**, a Generative AI application built as part of the **Generative AI using IBM Watsonx** course by the **IBM Career Education Program** in collaboration with **Vellore Institute of Technology (VIT)**.

InspireMe AI is an interactive text-generation application that uses advanced LLMs to generate personalized motivational quotes based on the user's current mood.

---

## 📖 Table of Contents
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Installation & Setup](#-installation--setup)
- [How It Works](#-how-it-works)
- [Course & Certification Info](#-course--certification-info)
- [License](#-license)

---

## 🎯 Project Overview

In today's fast-paced world, motivation is a driving force. InspireMe AI leverages open-source foundation models via local text generation pipelines to dynamically understand your mood (e.g., anxious, tired, happy, angry, sad) and instantly generate uplifting, context-specific quotes.

This repository contains the interactive Jupyter Notebook `InspireMeAI.ipynb` which demonstrates:
1. Loading state-of-the-art transformer pipelines.
2. Building dynamic prompt templates based on real-time user inputs.
3. Controlling LLM generation parameters (temperature, max_length, sampling) to produce diverse, meaningful text output.

---

## ⚡ Key Features

*   **Real-time Interaction:** Prompts the user to input their current state of mind.
*   **Dynamic Emoji Flair:** Automatically identifies the user's emotion and maps it to representative emojis.
*   **Pre-trained Transformer Model:** Utilizes **Google's FLAN-T5 Small** (a text-to-text transformer fine-tuned on a large collection of datasets).
*   **Parameter Optimization:** Configured with generation configurations like temperature scaling and sampling parameters to maintain quality and variety.
*   **Lightweight & Local:** Run directly inside your Jupyter environment without requiring expensive API keys.

---

## 🛠️ Tech Stack

*   **Language:** Python
*   **Libraries:**
    *   `transformers` (Hugging Face Hub interface)
    *   `sentencepiece` (Text tokenizer library)
    *   `torch` / PyTorch (Deep learning framework backend)
*   **Model:** [google/flan-t5-small](https://huggingface.co/google/flan-t5-small)
*   **Environment:** Jupyter Notebook / Google Colab / VS Code Jupyter Extension

---

## ⚙️ Installation & Setup

To run this project locally, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/ankit1207yadav/IBMGENAI.git
cd IBMGENAI
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
# Create a virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
Install the required packages using pip:
```bash
pip install transformers sentencepiece torch notebook
```

### 4. Run the Jupyter Notebook
Start the Jupyter Notebook server:
```bash
jupyter notebook
```
Open **`InspireMeAI.ipynb`** in your browser and run all cells sequentially.

---

## 🧠 How It Works

Here is a brief walkthrough of the pipeline execution in `InspireMeAI.ipynb`:

1.  **Dependency Installation & Setup:** Imports `pipeline` from Hugging Face's `transformers`.
2.  **Model Loading:** Downloads and loads `google/flan-t5-small` onto the local machine's CPU/GPU.
    ```python
    from transformers import pipeline
    generator = pipeline("text2text-generation", model="google/flan-t5-small")
    ```
3.  **User Input & Sentiment mapping:** Captures user feedback on their current emotion.
    ```text
    How are you feeling today (e.g., anxious, tired, happy)? Sad
    🎭 Mood: Sad 🧘
    ```
4.  **Prompt Engineering:** Wraps the input in a standard instruction prompt.
    ```python
    prompt = f"Give me a short motivational quote for someone who is feeling {mood}."
    ```
5.  **Generation & Output:** Generates and formats the quote.
    ```python
    response = generator(prompt, max_length=50, do_sample=True, temperature=0.8)
    ```

---

## 🎓 Course & Certification Info

This project was built during the **Generative AI using IBM Watsonx** course program.

*   **Offered by:** IBM Career Education Program
*   **In collaboration with:** VIT (Vellore Institute of Technology)
*   **Certificate Code:** `IBMCE CEWXAI1IN`
*   **Skills Acquired:** Hands-on experience with Generative AI tools, transformer architectures, local model inference pipelines, prompt engineering, and the IBM Watsonx ecosystem.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
