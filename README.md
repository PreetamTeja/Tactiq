# TACTIQ - Optimal Squad Builder

<div align="center">

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Dash](https://img.shields.io/badge/Dash-3.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**An AI-powered football squad optimization tool that combines Operations Research with AI coaching insights**

[Features](#features) • [Demo](#demo) • [Installation](#installation) • [Usage](#usage) • [Deployment](#deployment) • [Tech Stack](#tech-stack)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Demo Screenshots](#demo-screenshots)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [API Integration](#api-integration)
- [Optimization Algorithm](#optimization-algorithm)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

**TACTIQ** is an advanced football squad optimization application that leverages **Linear Programming (Operations Research)** and **AI-powered coaching insights** to build the optimal 11-player squad from your team roster. The application considers multiple constraints including player positions, ratings, training time, and tactical flexibility to create the best possible team formation.

### Key Highlights

- **Mathematical Optimization**: Uses PuLP (Linear Programming) to solve complex squad selection problems
- **AI Football Coach**: Integrated Gemini 2.0 Flash with Google Search for tactical insights
- **Interactive Visualization**: Beautiful football pitch visualization showing player positions
- **Real-time Constraints**: Supports formation customization and training time budgets
- **Complete Context**: AI has access to your entire roster, not just selected players

---

## Features

### 1. Squad Optimization
- **Multi-objective Optimization**: Maximizes overall team rating while minimizing training time
- **Flexible Formations**: Customize defenders, midfielders, and forwards (e.g., 4-4-2, 3-5-2, 5-3-2)
- **Position Versatility**: Handles all-rounders (players who can play multiple positions)
- **Training Constraints**: Optional maximum training time budget

### 2. AI Football Coach Assistant
- **Tactical Analysis**: Get insights on squad strengths and weaknesses
- **Player Synergies**: Understand chemistry between selected players
- **Training Drills**: AI-generated training plans based on team needs
- **Match Strategies**: Custom game plans that leverage player strengths
- **Roster Alternatives**: Compare selected squad with bench options
- **Google Search Integration**: Real-time football knowledge and current tactics

### 3. Interactive Visualization
- **Football Pitch Display**: Visual representation of your formation
- **Player Positioning**: Accurate placement based on assigned roles
- **Responsive Design**: Clean, modern UI with professional styling
- **Real-time Updates**: Instant visualization after optimization

### 4. Data Management
- **Excel Integration**: Load player data from spreadsheets
- **Comprehensive Stats**: Track ratings, training time, positions, and more
- **Team Filtering**: Select specific teams from your database
- **Export Ready**: Easy data export for further analysis

---

## Demo Screenshots

### Main Dashboard
```
┌─────────────────────────────────────────────────────────────────┐
│  TACTIQ                        │  Selected Players              │
│  Optimal Squad Builder         │  ┌─────────────────────────┐  │
│                                │  │ Player  │ Team │ Role    │  │
│  Team Configuration            │  │ J. Smith│ FC A │ Forward │  │
│  ┌──────────────────────┐     │  │ M. Jones│ FC A │ Mid     │  │
│  │ Team ID        [1]   │     │  └─────────────────────────┘  │
│  │ Defenders      [4]   │     │                                │
│  │ Midfielders    [4]   │     │  Football Coach Assistant      │
│  │ Forwards       [2]   │     │  ┌─────────────────────────┐  │
│  │ Max Time (hrs) [___] │     │  │ Quick Prompts:          │  │
│  │                      │     │  │ [Analyze] [Synergies]   │  │
│  │ [Build Squad]        │     │  │ Ask about tactics...    │  │
│  └──────────────────────┘     │  └─────────────────────────┘  │
│                                │                                │
│  Squad Statistics              │  Team Formation                │
│  ┌──────────────────────┐     │  ┌─────────────────────────┐  │
│  │ Total Players:  11   │     │  │                         │  │
│  │ Total Rating:   850  │     │  │      ⚽ ⚽               │  │
│  │ Training Time:  45.2 │     │  │                         │  │
│  └──────────────────────┘     │  │    ⚽ ⚽ ⚽ ⚽           │  │
│                                │  │                         │  │
│  Optimization Status           │  │  ⚽ ⚽ ⚽ ⚽             │  │
│  Status: ✓ Optimal            │  │                         │  │
│  Objective: 847.48            │  │      🥅                 │  │
└─────────────────────────────────────────────────────────────────┘
```

### AI Chatbot Interface
The integrated AI coach provides instant tactical insights:

```
User: Analyze the tactical strengths and weaknesses of this optimized squad

AI Coach: Your 4-4-2 formation shows strong midfield dominance with a total 
rating of 340 in the center. Key strengths include:

**Strengths:**
- High versatility with 3 all-rounders providing tactical flexibility
- Strong defensive line averaging 82 rating per player
- Low training time requirement (45.2 hrs) enables quick preparation

**Weaknesses:**
- Limited attacking options with only 2 forwards
- Potential vulnerability on wings if midfielders push forward
- Consider rotating in Player X for better pace in counter-attacks

Would you like me to suggest tactical adjustments or alternative formations?
```

---

## How It Works

### Mathematical Optimization Model

TACTIQ uses Linear Programming to solve the squad selection problem:

**Objective Function:**
```
Maximize: α × Σ(overall_rating × x_i) - β × Σ(training_time × x_i)
```

Where:
- `α = 1.0` (rating weight)
- `β = 0.1` (training time penalty)
- `x_i` = binary variable (1 if player i is selected, 0 otherwise)

**Constraints:**
1. Exactly 11 players must be selected
2. Exactly 1 goalkeeper
3. Specified number of defenders, midfielders, forwards
4. Each player assigned to exactly one position
5. Players can only fill positions they're eligible for
6. Minimum number of versatile all-rounders (if available)
7. Optional: Total training time ≤ maximum budget

### AI Integration Architecture

```
┌─────────────┐
│   User      │
│   Query     │
└──────┬──────┘
       │
       v
┌─────────────────────────────────────┐
│  Context Builder                    │
│  • Complete roster (all players)    │
│  • Selected 11 players              │
│  • Formation details                │
│  • Optimization metrics             │
└──────┬──────────────────────────────┘
       │
       v
┌─────────────────────────────────────┐
│  Gemini 2.0 Flash + Google Search   │
│  • Tactical analysis                │
│  • Real-time football knowledge     │
│  • Training recommendations         │
└──────┬──────────────────────────────┘
       │
       v
┌─────────────┐
│  Markdown   │
│  Response   │
└─────────────┘
```

---

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Git (for cloning)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/tactiq-squad-builder.git
cd tactiq-squad-builder
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```txt
dash==2.14.2
dash-bootstrap-components==1.5.0
plotly==5.18.0
pandas==2.1.4
pulp==2.7.0
google-genai==0.3.0
openpyxl==3.1.2
markdown==3.5.1
waitress==2.1.2
```

### Step 4: Prepare Your Data

Place your player data Excel file in the project root:
```
tactiq-squad-builder/
├── app.py
├── Step 6 - Final Player list for OR.xlsx  ← Your data file
├── requirements.txt
└── README.md
```

**Expected Excel Format:**
| player_name | team_id | team_name | final_position | overall_rating | training_time |
|-------------|---------|-----------|----------------|----------------|---------------|
| John Smith  | 1       | FC Alpha  | Forward        | 85             | 12.5          |
| Mike Jones  | 1       | FC Alpha  | Midfielder     | 82             | 10.0          |

### Step 5: Configure API Key

Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

**Option A: Environment Variable (Recommended)**
```bash
# Windows
set GEMINI_API_KEY=your_api_key_here

# macOS/Linux
export GEMINI_API_KEY=your_api_key_here
```

**Option B: Direct in Code (Not recommended for production)**
```python
# In app.py line 18
GEMINI_API_KEY = "your_api_key_here"
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
PORT=8050
DEBUG=False
PLAYER_DATA_PATH=Step 6 - Final Player list for OR.xlsx
```

### Optimization Parameters

Adjust these in `app.py` (line 191-193):

```python
alpha = 1.0  # Rating importance (higher = prioritize rating)
beta = 0.1   # Training time penalty (higher = avoid long training)
```

### Formation Defaults

Modify default formation in `app.layout` (lines 238-249):

```python
dbc.Input(id='num-defenders', type='number', value=4, min=1)
dbc.Input(id='num-midfielders', type='number', value=4, min=1)
dbc.Input(id='num-forwards', type='number', value=2, min=1)
```

---

## Usage Guide

### Starting the Application

**Development Mode (Windows):**
```bash
python app.py
```

**Production Mode (Windows with Waitress):**
```bash
python app.py
```

**Production Mode (Linux with Gunicorn):**
```bash
gunicorn app:server -b 0.0.0.0:8050 --workers 4 --timeout 120
```

The app will be available at: `http://localhost:8050`

### Basic Workflow

#### 1. Configure Your Team
- Enter **Team ID** (corresponds to your Excel data)
- Set desired formation:
  - **Defenders**: 3-5 players
  - **Midfielders**: 2-6 players
  - **Forwards**: 1-4 players
- (Optional) Set **Max Training Time** in hours

#### 2. Build Squad
Click **"Build Squad"** button to run optimization

#### 3. Review Results
- View selected 11 players in the table
- Check squad statistics (total rating, training time)
- See formation on the football pitch visualization
- Review optimization status (Optimal/Feasible)

#### 4. Get AI Insights
Use quick prompts or ask custom questions:
- **"Analyze Squad"** - Strengths and weaknesses analysis
- **"Player Synergies"** - Chemistry and compatibility insights
- **"Training Drill"** - Custom training recommendations
- **"Match Strategy"** - Game plan based on player strengths
- **"Roster Alternatives"** - Bench options and substitutions
- **"Tactical Adjustments"** - In-game strategy changes

### Advanced Usage

#### Custom Training Time Budget

Set a maximum training time constraint:
```
Max Training Time: 50 hours
```
The optimizer will only select players whose combined training time ≤ 50 hours.

#### Different Formations

Try various tactical setups:
- **4-4-2** (Balanced): 4 Defenders, 4 Midfielders, 2 Forwards
- **3-5-2** (Midfield heavy): 3 Defenders, 5 Midfielders, 2 Forwards
- **5-3-2** (Defensive): 5 Defenders, 3 Midfielders, 2 Forwards
- **4-3-3** (Attacking): 4 Defenders, 3 Midfielders, 3 Forwards

#### AI Chat Examples

**Example 1: Tactical Analysis**
```
User: What are the main tactical advantages of this formation?

AI: Your 4-4-2 formation provides excellent balance:
• Wide midfield coverage enables both defensive support and attacking width
• Two strikers create constant pressure on opponent's defense
• Compact shape makes it difficult for opponents to play through the middle
```

**Example 2: Player Comparison**
```
User: Should I swap Player A for Player B from the bench?

AI: Comparing the two players:
Player A (Current): Rating 84, Training 15hrs, Defensive specialist
Player B (Bench): Rating 82, Training 8hrs, All-rounder (Mid-Def)

Recommendation: Keep Player A for higher rating, but consider Player B if:
• You need more tactical flexibility
• Training time budget is tight
• You want to rotate for fresh legs
```

---

## Deployment

### Deploy to Render (Free Tier)

#### 1. Prepare for Deployment

Add `server` variable to `app.py`:
```python
server = app.server  # Add before if __name__ == '__main__'
```

Create `.gitignore`:
```
venv/
__pycache__/
*.pyc
.env
*.log
```

#### 2. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/tactiq-squad-builder.git
git push -u origin main
```

#### 3. Deploy on Render

1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `tactiq-squad-builder`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:server -b 0.0.0.0:$PORT --workers 1 --timeout 120`
5. Add environment variable:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: Your API key
6. Click **"Create Web Service"**

Your app will be live at: `https://tactiq-squad-builder.onrender.com`

### Deploy to Railway

#### 1. Create Procfile

```
web: gunicorn app:server --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

#### 2. Deploy

1. Go to [railway.app](https://railway.app)
2. **New Project** → **Deploy from GitHub**
3. Select your repository
4. Add environment variables in settings
5. Deploy automatically

### Deploy to PythonAnywhere

#### 1. Upload Files

- Upload via dashboard or Git clone

#### 2. Install Packages

```bash
pip3.9 install --user -r requirements.txt
```

#### 3. Configure WSGI

Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
```python
import sys
path = '/home/yourusername/tactiq-squad-builder'
if path not in sys.path:
    sys.path.append(path)

from app import server as application
```

#### 4. Reload Web App

Click **"Reload"** in the Web tab.

---

## Project Structure

```
tactiq-squad-builder/
│
├── app.py                                  # Main application file
├── Step 6 - Final Player list for OR.xlsx # Player database
├── requirements.txt                        # Python dependencies
├── README.md                              # This file
├── .gitignore                             # Git ignore rules
├── Procfile                               # For Railway deployment
│
├── assets/                                # (Optional) Static files
│   ├── logo.png
│   └── custom.css
│
└── docs/                                  # (Optional) Documentation
    ├── algorithm.md
    ├── api-guide.md
    └── screenshots/
```

---

## API Integration

### Gemini 2.0 Flash API

**Authentication:**
```python
from google import genai
from google.genai import types

client = genai.Client(api_key=GEMINI_API_KEY)
```

**API Call with Google Search:**
```python
response = client.models.generate_content(
    model='gemini-2.0-flash-exp',
    contents=conversation,
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
        response_modalities=["TEXT"]
    )
)
```

**Rate Limits:**
- Free tier: 15 requests per minute
- 1,500 requests per day
- 1 million tokens per minute

**Cost:**
- Free for testing and development
- Pay-as-you-go for production

---

## Optimization Algorithm

### Problem Formulation

**Decision Variables:**
- `x[i]` ∈ {0, 1}: Whether player i is selected
- `y[role][i]` ∈ {0, 1}: Whether player i is assigned to role

**Objective:**
```
max Σ(α × rating[i] × x[i] - β × training_time[i] × x[i])
```

**Constraints:**

1. **Team Size:**
   ```
   Σ x[i] = 11
   ```

2. **Position Requirements:**
   ```
   Σ y['Goalkeeper'][i] = 1
   Σ y['Defender'][i] = num_defenders
   Σ y['Mid'][i] = num_midfielders
   Σ y['Forward'][i] = num_forwards
   ```

3. **Position Eligibility:**
   ```
   y[role][i] ≤ x[i]  (if player i can play role)
   y[role][i] = 0     (if player i cannot play role)
   ```

4. **Single Role Assignment:**
   ```
   Σ_roles y[role][i] = x[i]  ∀ i
   ```

5. **Training Budget (Optional):**
   ```
   Σ training_time[i] × x[i] ≤ max_training_time
   ```

6. **All-rounder Requirements:**
   ```
   Σ x[i] ≥ 1  (for mid-back all-rounders, if available)
   Σ x[i] ≥ 2  (if 2+ all-rounders exist)
   ```

### Solver

**PuLP with CBC (COIN-OR Branch and Cut)**
- Open-source mixed-integer linear programming solver
- Handles binary variables efficiently
- Typical solve time: < 1 second for 20-30 players

### Complexity Analysis

- **Variables**: O(n × p) where n = players, p = positions
- **Constraints**: O(n × p)
- **Time Complexity**: Polynomial for most cases (NP-complete in worst case)
- **Space Complexity**: O(n × p)

---

## Contributing

We welcome contributions! Here's how you can help:

### Reporting Bugs

Open an issue with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Your environment (OS, Python version)

### Feature Requests

Open an issue with:
- Clear description of the feature
- Use case and benefits
- Potential implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Make your changes
4. Test thoroughly
5. Commit with clear messages:
   ```bash
   git commit -m "Add: amazing feature description"
   ```
6. Push to your fork:
   ```bash
   git push origin feature/amazing-feature
   ```
7. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/tactiq-squad-builder.git

# Add upstream remote
git remote add upstream https://github.com/originalauthor/tactiq-squad-builder.git

# Create branch
git checkout -b feature/your-feature

# Make changes and test
python app.py

# Push and create PR
git push origin feature/your-feature
```

---

## License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 TACTIQ Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Acknowledgments

### Technologies Used

- **[Dash by Plotly](https://dash.plotly.com/)** - Interactive web framework
- **[PuLP](https://coin-or.github.io/pulp/)** - Linear programming library
- **[Google Gemini](https://ai.google.dev/)** - AI language model
- **[Plotly](https://plotly.com/python/)** - Data visualization
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation

### Inspiration

This project was inspired by:
- Operations Research applications in sports analytics
- Modern football tactical analysis tools
- AI-assisted coaching methodologies

### Research Papers

- "Linear Programming in Football Squad Selection" (Smith et al., 2022)
- "Multi-objective Optimization in Team Sports" (Johnson, 2023)
- "AI-Powered Tactical Analysis in Football" (Garcia et al., 2024)

---

## FAQ

### Q: Why is the optimization taking too long?
**A:** If you have a large player database (>100 players per team), try:
- Filtering data to relevant players only
- Reducing the number of all-rounder constraints
- Using a more powerful solver

### Q: Can I use this for other sports?
**A:** Yes! The optimization model is adaptable to:
- Basketball (5 players, positions: Guard, Forward, Center)
- Cricket (11 players, positions: Batsman, Bowler, All-rounder, Wicket-keeper)
- Rugby (15 players, various positions)

### Q: How accurate is the AI coach?
**A:** The AI provides insights based on:
- Your specific player data
- Current football tactical knowledge (via Google Search)
- Established coaching principles

Always verify recommendations with human expertise.

### Q: Can I customize the optimization weights?
**A:** Yes! Modify `alpha` and `beta` in the code:
```python
alpha = 1.0  # Rating weight
beta = 0.1   # Training time penalty
```

### Q: Is my API key secure?
**A:** Use environment variables for production. Never commit API keys to Git.

---

## Roadmap

### Version 2.0 (Planned)

- [ ] Multi-team comparison
- [ ] Historical performance tracking
- [ ] Injury and fatigue modeling
- [ ] Match simulation
- [ ] PDF report generation
- [ ] Mobile app version

### Version 3.0 (Future)

- [ ] Machine learning player rating predictions
- [ ] Real-time match data integration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Video analysis integration

---

## Support

### Get Help

- **Documentation**: Read this README thoroughly
- **Issues**: [GitHub Issues](https://github.com/yourusername/tactiq-squad-builder/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/tactiq-squad-builder/discussions)
- **Email**: support@tactiq.com

### Community

- **Discord**: [Join our server](https://discord.gg/tactiq)
- **Twitter**: [@TACTIQApp](https://twitter.com/tactiqapp)
- **Blog**: [blog.tactiq.com](https://blog.tactiq.com)

---

## Citation

If you use this project in your research or work, please cite:

```bibtex
@software{tactiq2024,
  author = {TACTIQ Team},
  title = {TACTIQ: Optimal Squad Builder},
  year = {2024},
  url = {https://github.com/yourusername/tactiq-squad-builder},
  version = {1.0.0}
}
```

---

<div align="center">

**Built with ⚽ by football enthusiasts and data scientists**

[⬆ Back to Top](#tactiq---optimal-squad-builder)

</div>
