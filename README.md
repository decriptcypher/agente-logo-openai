# AI Branding Agent

An AI-powered system that automatically generates a complete brand identity.

Starting from a simple idea, the agent creates:

* Brand identity
* Logo
* Marketing visuals
* Social media assets
* Product packaging mockups

The goal is to transform a basic brand description into a **visual media kit** automatically.

---

# How It Works

The system follows a simple generation pipeline:

Brand Idea
↓
Brand Identity Generation
↓
Logo Generation
↓
Media Asset Generation
↓
Complete Brand Media Kit

Each step uses AI to maintain visual consistency across the generated assets.

---

# Features

The agent can automatically generate:

* Brand identity description
* Logo
* Business card mockup
* Promotional merchandise
* Corporate stationery
* Instagram promotional post
* Instagram institutional post
* Product packaging
* Advertising-style packaging mockup

All assets follow the same branding rules and visual style.

---

# Tech Stack

* Python
* Streamlit
* OpenAI API
* AI Image Generation

---

# Project Structure

app.py
Streamlit interface for interacting with the agent.

main.py
Core logic for branding, logo generation, and media kit generation.

agents/
Modules responsible for different generation steps.

---

# Running the Project

Install dependencies:

pip install -r requirements.txt

Run the interface:

streamlit run app.py

The app will start locally and open in your browser.

---

# Configuration

Set your OpenAI API key before running the project:

export OPENAI_API_KEY="your-api-key"

---

# Example Workflow

1. Enter the brand name
2. Provide a short description of the brand
3. The system generates:

   * brand identity
   * logo
   * media kit
   * marketing visuals

---

# Future Improvements

* Style Guide generation
* More media mockups
* Brand asset export
* Automatic brand book generation
* Online deployment

---

# License

MIT
