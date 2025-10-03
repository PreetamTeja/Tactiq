import dash
from dash import dcc, html, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import pulp
from google import genai
from google.genai import types
import math
import markdown

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "TACTIQ"

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyBSEaknAfxR7vH04Rtts8Wi082DMGWlLmA"
client = genai.Client(api_key=GEMINI_API_KEY)

# Load player data
PLAYER_DATA_PATH = "Database.xlsx"
print("Loading player data...")
try:
    PLAYER_DATA = pd.read_excel(PLAYER_DATA_PATH)
    print(f"✓ Loaded {len(PLAYER_DATA)} players from {PLAYER_DATA_PATH}")
except Exception as e:
    print(f"✗ Error loading player data: {e}")
    PLAYER_DATA = None

# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: #ffffff;
                margin: 0;
                padding: 0;
            }
            .sidebar {
                background: white;
                box-shadow: 2px 0 8px rgba(0,0,0,0.1);
                height: 100vh;
                overflow-y: auto;
                position: fixed;
                width: 320px;
                border-right: 1px solid #e0e0e0;
            }
            .main-content {
                margin-left: 320px;
                padding: 32px;
                min-height: 100vh;
                background: #ffffff;
            }
            .card-modern {
                background: white;
                border-radius: 8px;
                border: 1px solid #000000;
                padding: 24px;
                margin-bottom: 20px;
            }
            .input-modern {
                border: 1px solid #000000;
                border-radius: 6px;
                padding: 10px 12px;
                font-size: 14px;
                transition: all 0.2s;
                background: white;
            }
            .input-modern:focus {
                border-color: #2c3e50;
                box-shadow: 0 0 0 3px rgba(44, 62, 80, 0.1);
            }
            .btn-primary-modern {
                background: #2c3e50;
                border: 1px solid #000000;
                border-radius: 6px;
                padding: 12px 24px;
                font-weight: 600;
                transition: all 0.3s;
                color: white;
            }
            .btn-primary-modern:hover {
                background: #1a252f;
                transform: translateY(-1px);
            }
            .stat-card {
                text-align: center;
                padding: 16px;
                background: white;
                border: 1px solid #000000;
                border-radius: 8px;
                margin-bottom: 12px;
            }
            .stat-value {
                font-size: 28px;
                font-weight: 700;
                color: #2c3e50;
                margin: 4px 0;
            }
            .stat-label {
                font-size: 10px;
                color: #7f8c8d;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 600;
            }
            .section-title {
                font-size: 16px;
                font-weight: 700;
                color: #2c3e50;
                margin-bottom: 16px;
            }
            .badge-success {
                background: #27ae60;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }
            .badge-warning {
                background: #e67e22;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }
            .pitch-container {
                background: white;
                border-radius: 8px;
                padding: 24px;
                border: 1px solid #000000;
            }
            .app-logo {
                font-size: 32px;
                font-weight: 900;
                color: #2c3e50;
                margin-bottom: 8px;
                letter-spacing: -1px;
            }
            .app-subtitle {
                font-size: 12px;
                color: #7f8c8d;
                text-transform: uppercase;
                letter-spacing: 2px;
                font-weight: 600;
                margin-bottom: 32px;
            }
            .chat-container {
                border: 1px solid #000000;
                border-radius: 8px;
                background: white;
                padding: 16px;
                height: 300px;
                display: flex;
                flex-direction: column;
            }
            .chat-messages {
                flex: 1;
                overflow-y: auto;
                margin-bottom: 12px;
                padding: 12px;
                background: #f8f9fa;
                border-radius: 6px;
                max-height: 200px;
            }
            .chat-message {
                margin-bottom: 12px;
                padding: 8px 12px;
                border-radius: 6px;
            }
            .user-message {
                background: #2c3e50;
                color: white;
                margin-left: 20px;
            }
            .bot-message {
                background: white;
                border: 1px solid #e0e0e0;
                margin-right: 20px;
            }
            .bot-message p {
                margin: 8px 0;
            }
            .bot-message strong {
                font-weight: 700;
                color: #2c3e50;
            }
            .bot-message em {
                font-style: italic;
            }
            .bot-message ul, .bot-message ol {
                margin: 8px 0;
                padding-left: 24px;
            }
            .bot-message li {
                margin: 4px 0;
            }
            .bot-message code {
                background: #f0f0f0;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
            .bot-message pre {
                background: #f0f0f0;
                padding: 12px;
                border-radius: 4px;
                overflow-x: auto;
                margin: 8px 0;
            }
            .bot-message h3 {
                font-size: 14px;
                font-weight: 700;
                margin: 12px 0 6px 0;
                color: #2c3e50;
            }
            .chat-input-container {
                display: flex;
                gap: 8px;
            }
            .prompt-button {
                fontSize: 10px;
                padding: 4px 8px;
                marginRight: 4px;
                marginBottom: 4px;
                border: 1px solid #ddd;
                borderRadius: 4px;
                background: white;
                cursor: pointer;
            }
            .prompt-button:hover {
                background: #f0f0f0 !important;
                border-color: #2c3e50 !important;
                transition: all 0.2s;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App layout
app.layout = html.Div([
    # Sidebar
    html.Div([
        html.Div([
            html.Div("TACTIQ", className="app-logo", style={"textAlign": "center"}),
            html.Div("Optimal Squad Builder", className="app-subtitle", style={"textAlign": "center"}),
            
            # Configuration Form
            html.Div([
                html.Label("Team Configuration", className="section-title"),
                
                html.Div([
                    html.Label("Team ID", style={'fontSize': '13px', 'color': '#2c3e50', 'fontWeight': '600', 'marginBottom': '6px', 'display': 'block'}),
                    dbc.Input(id='team-id', type='number', value=1, min=1, className='input-modern')
                ], style={'marginBottom': '20px'}),
                
                html.Div([
                    html.Label("Goalkeepers", style={'fontSize': '13px', 'color': '#2c3e50', 'fontWeight': '600', 'marginBottom': '6px', 'display': 'block'}),
                    dbc.Input(id='num-gk', type='number', value=1, disabled=True, className='input-modern', style={'background': '#f8f9fa'})
                ], style={'marginBottom': '20px'}),
                
                html.Div([
                    html.Label("Defenders", style={'fontSize': '13px', 'color': '#2c3e50', 'fontWeight': '600', 'marginBottom': '6px', 'display': 'block'}),
                    dbc.Input(id='num-defenders', type='number', value=4, min=1, className='input-modern')
                ], style={'marginBottom': '20px'}),
                
                html.Div([
                    html.Label("Midfielders", style={'fontSize': '13px', 'color': '#2c3e50', 'fontWeight': '600', 'marginBottom': '6px', 'display': 'block'}),
                    dbc.Input(id='num-midfielders', type='number', value=4, min=1, className='input-modern')
                ], style={'marginBottom': '20px'}),
                
                html.Div([
                    html.Label("Forwards", style={'fontSize': '13px', 'color': '#2c3e50', 'fontWeight': '600', 'marginBottom': '6px', 'display': 'block'}),
                    dbc.Input(id='num-forwards', type='number', value=2, min=1, className='input-modern')
                ], style={'marginBottom': '20px'}),
                
                # Max Training Time Constraint
                html.Div([
                    html.Label("Max Training Time (hours)", style={'fontSize': '13px', 'color': '#2c3e50', 'fontWeight': '600', 'marginBottom': '6px', 'display': 'block'}),
                    html.Div([
                        dbc.Input(id='max-training-time', type='number', min=0, placeholder='Leave empty for no limit', className='input-modern')
                    ]),
                    html.Small("", style={'fontSize': '11px', 'color': '#7f8c8d', 'marginTop': '4px', 'display': 'block'})
                ], style={'marginBottom': '24px'}),
                
                html.Button("Build Squad", id='optimize-btn', className='btn-primary-modern', 
                           style={'width': '100%', 'fontSize': '15px'})
            ], style={'marginBottom': '24px'}),
            
            # Stats Cards
            html.Div(id='stats-container'),
            
            # Optimality Check
            html.Div(id='optimality-container')
            
        ], style={'padding': '32px'})
    ], className='sidebar'),
    
    # Main Content
    html.Div([
        html.Div(id='results-container')
    ], className='main-content'),
    
    # Store for chat history and team data
    dcc.Store(id='chat-history', data=[]),
    dcc.Store(id='selected-team-data', data=None),
    dcc.Store(id='all-team-players-data', data=None)
])

def run_optimization(df, team_id, num_defenders, num_midfielders, num_forwards, max_training_time=None):
    """Run the optimization algorithm with optional training time constraint"""
    num_goalkeepers = 1
    alpha = 1.0
    beta = 0.1
    
    team_df = df[df["team_id"] == team_id].reset_index(drop=True)
    if team_df.empty:
        return None, "No players found for the selected Team ID"
    
    if not any(team_df["final_position"].str.contains("Goalkeeper", case=False, na=False)):
        return None, f"Team {team_id} has no eligible Goalkeeper!"
    
    position_map = {
        "Forward": ["Forward"],
        "Midfielder": ["Mid"],
        "Defender": ["Defender"],
        "Goalkeeper": ["Goalkeeper"],
        "Forward-Mid All-rounder": ["Forward", "Mid"],
        "Mid-Back All-rounder": ["Mid", "Defender"],
        "All All-rounder": ["Forward", "Mid", "Defender"]
    }
    
    players = team_df.index.tolist()
    roles = ["Defender", "Mid", "Forward", "Goalkeeper"]
    
    x = pulp.LpVariable.dicts("player", players, cat='Binary')
    y = {role: pulp.LpVariable.dicts(role, players, cat='Binary') for role in roles}
    
    prob = pulp.LpProblem("Team_Selection", pulp.LpMaximize)
    
    prob += pulp.lpSum([
        alpha * team_df.loc[i, "overall_rating"] * x[i] -
        beta * team_df.loc[i, "training_time"] * x[i] for i in players
    ])
    
    for role in roles:
        for i in players:
            if role in position_map.get(team_df.loc[i, "final_position"], []):
                prob += y[role][i] <= x[i]
            else:
                prob += y[role][i] == 0
    
    for i in players:
        prob += pulp.lpSum([y[role][i] for role in roles]) == x[i]
    
    prob += pulp.lpSum([y["Defender"][i] for i in players]) == num_defenders
    prob += pulp.lpSum([y["Mid"][i] for i in players]) == num_midfielders
    prob += pulp.lpSum([y["Forward"][i] for i in players]) == num_forwards
    prob += pulp.lpSum([y["Goalkeeper"][i] for i in players]) == num_goalkeepers
    prob += pulp.lpSum([x[i] for i in players]) == num_defenders + num_midfielders + num_forwards + num_goalkeepers
    
    # Add training time constraint if specified
    if max_training_time is not None and max_training_time > 0:
        prob += pulp.lpSum([team_df.loc[i, "training_time"] * x[i] for i in players]) <= max_training_time
    
    mid_all_rounders = [i for i in players if "Mid" in position_map.get(team_df.loc[i, "final_position"], []) and "Defender" in position_map.get(team_df.loc[i, "final_position"], [])]
    def_all_rounders = [i for i in players if "Defender" in position_map.get(team_df.loc[i, "final_position"], []) and "Mid" in position_map.get(team_df.loc[i, "final_position"], [])]
    
    if len(mid_all_rounders) >= 1:
        prob += pulp.lpSum([x[i] for i in mid_all_rounders]) >= 1
    if len(mid_all_rounders) >= 2:
        prob += pulp.lpSum([x[i] for i in mid_all_rounders]) >= 2
    if len(def_all_rounders) >= 1:
        prob += pulp.lpSum([x[i] for i in def_all_rounders]) >= 1
    if len(def_all_rounders) >= 2:
        prob += pulp.lpSum([x[i] for i in def_all_rounders]) >= 2
    
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    
    selected_data = []
    for i in players:
        if pulp.value(x[i]) == 1:
            assigned_role = None
            for role in roles:
                if pulp.value(y[role][i]) == 1:
                    assigned_role = role
                    break
            
            selected_data.append({
                'player_name': team_df.loc[i, 'player_name'],
                'team_name': team_df.loc[i, 'team_name'] if 'team_name' in team_df.columns else 'N/A',
                'final_position': team_df.loc[i, 'final_position'],
                'assigned_role': assigned_role,
                'overall_rating': team_df.loc[i, 'overall_rating'],
                'training_time': team_df.loc[i, 'training_time']
            })
    
    selected_df = pd.DataFrame(selected_data)
    status = pulp.LpStatus[prob.status]
    objective_value = pulp.value(prob.objective)
    
    return selected_df, status, objective_value

def create_vertical_pitch(selected_df):
    """Create vertical football pitch with player positions"""
    fig = go.Figure()
    
    # Vertical pitch dimensions
    pitch_width = 60
    pitch_height = 90
    
    # Draw pitch background
    fig.add_shape(type="rect", x0=0, y0=0, x1=pitch_width, y1=pitch_height,
                  fillcolor="#1a7f3e", line=dict(color="white", width=3))
    
    # Halfway line
    fig.add_shape(type="line", x0=0, y0=pitch_height/2, x1=pitch_width, y1=pitch_height/2,
                  line=dict(color="white", width=2))
    
    # Center circle
    fig.add_shape(type="circle", 
                  x0=pitch_width/2-8, y0=pitch_height/2-8,
                  x1=pitch_width/2+8, y1=pitch_height/2+8,
                  line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)")
    
    # Center spot
    fig.add_shape(type="circle", 
                  x0=pitch_width/2-0.7, y0=pitch_height/2-0.7,
                  x1=pitch_width/2+0.7, y1=pitch_height/2+0.7,
                  fillcolor="white", line=dict(color="white", width=0))
    
    # Bottom penalty area (our goal)
    fig.add_shape(type="rect", x0=12, y0=0, x1=pitch_width-12, y1=14,
                  line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)")
    
    # Top penalty area (opponent goal)
    fig.add_shape(type="rect", x0=12, y0=pitch_height-14, x1=pitch_width-12, y1=pitch_height,
                  line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)")
    
    # Bottom goal area (6-yard box)
    fig.add_shape(type="rect", x0=21, y0=0, x1=pitch_width-21, y1=5,
                  line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)")
    
    # Top goal area (6-yard box)
    fig.add_shape(type="rect", x0=21, y0=pitch_height-5, x1=pitch_width-21, y1=pitch_height,
                  line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)")
    
    # Penalty spots
    fig.add_shape(type="circle", x0=pitch_width/2-0.7, y0=10-0.7,
                  x1=pitch_width/2+0.7, y1=10+0.7,
                  fillcolor="white", line=dict(color="white", width=0))
    fig.add_shape(type="circle", x0=pitch_width/2-0.7, y0=pitch_height-10-0.7,
                  x1=pitch_width/2+0.7, y1=pitch_height-10+0.7,
                  fillcolor="white", line=dict(color="white", width=0))
    
    # Plot players if data available
    if selected_df is not None and len(selected_df) > 0:
        positions = {
            'Goalkeeper': [],
            'Defender': [],
            'Mid': [],
            'Forward': []
        }
        
        for idx, player in selected_df.iterrows():
            role = player['assigned_role'] if 'assigned_role' in player else None
            name = player['player_name'] if 'player_name' in player else f"Player {idx}"
            
            if role in positions:
                positions[role].append(name)
        
        all_x = []
        all_y = []
        all_names = []
        
        # Goalkeeper (bottom - defending)
        for i, player_name in enumerate(positions['Goalkeeper']):
            all_x.append(pitch_width / 2)
            all_y.append(8)
            all_names.append(player_name)
        
        # Defenders (bottom third)
        num_def = len(positions['Defender'])
        if num_def > 0:
            spacing = pitch_width / (num_def + 1)
            for i, player_name in enumerate(positions['Defender']):
                x = spacing * (i + 1)
                all_x.append(x)
                all_y.append(22)
                all_names.append(player_name)
        
        # Midfielders (middle third)
        num_mid = len(positions['Mid'])
        if num_mid > 0:
            spacing = pitch_width / (num_mid + 1)
            for i, player_name in enumerate(positions['Mid']):
                x = spacing * (i + 1)
                all_x.append(x)
                all_y.append(45)
                all_names.append(player_name)
        
        # Forwards (top third - attacking)
        num_fwd = len(positions['Forward'])
        if num_fwd > 0:
            spacing = pitch_width / (num_fwd + 1)
            for i, player_name in enumerate(positions['Forward']):
                x = spacing * (i + 1)
                all_x.append(x)
                all_y.append(68)
                all_names.append(player_name)
        
        # Add player icons as SVG stick figures
        for i in range(len(all_x)):
            x, y = all_x[i], all_y[i]
            
            # Head
            fig.add_shape(
                type="circle",
                x0=x-0.8, y0=y+1.5,
                x1=x+0.8, y1=y+3.1,
                fillcolor='#1e293b',
                line=dict(color='#1e293b', width=1),
                layer='above'
            )
            
            # Body
            fig.add_shape(
                type="line",
                x0=x, y0=y+1.5,
                x1=x, y1=y-1.5,
                line=dict(color='#1e293b', width=2.5),
                layer='above'
            )
            
            # Arms
            fig.add_shape(
                type="line",
                x0=x-1.5, y0=y+0.5,
                x1=x+1.5, y1=y+0.5,
                line=dict(color='#1e293b', width=2.5),
                layer='above'
            )
        
        # Add player names
        if len(all_x) > 0:
            fig.add_trace(go.Scatter(
                x=all_x,
                y=[y - 3 for y in all_y],
                mode='text',
                text=all_names,
                textfont=dict(
                    size=7,
                    color='white',
                    family='Arial Black'
                ),
                showlegend=False,
                hoverinfo='text',
                hovertext=all_names
            ))
    
    # Update layout
    fig.update_layout(
        xaxis=dict(range=[-2, pitch_width+2], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-2, pitch_height+2], showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='#1a7f3e',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20),
        height=900,
        shapes=[shape for shape in fig.layout.shapes]
    )
    
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True, scaleanchor="x", scaleratio=1)
    
    for trace in fig.data:
        trace.update(visible=True)
    
    return fig

def get_football_assistant_response(user_message, chat_history, team_data=None, all_team_players=None):
    """Get response from Gemini with football-specific guardrails, team context, and Google Search"""
    
    system_prompt = """You are a professional football coach assistant with deep knowledge of tactics, formations, player performance, and team strategies. 

STRICT RULES:
1. ONLY answer questions related to football/soccer (tactics, formations, players, teams, training, strategies, match analysis)
2. If asked about non-football topics, politely redirect: "I'm specialized in football coaching and tactics. Please ask me about formations, players, team strategies, or match analysis."
3. Keep responses concise (2-3 paragraphs maximum)
4. Be professional and insightful
5. Base advice on established football principles
6. You have access to Google Search - use it when you need current information about players, teams, tactics, or recent matches

You can discuss:
- Team formations and tactics
- Player positioning and roles
- Match strategies and analysis
- Training methods
- Player synergy and chemistry
- Historical team performance
- Tactical adjustments
"""

    # Add ALL team players context
    if all_team_players is not None and len(all_team_players) > 0:
        system_prompt += f"""

COMPLETE TEAM ROSTER (All {len(all_team_players)} available players):
"""
        for player in all_team_players:
            system_prompt += f"- {player['player_name']} ({player['team_name']}) - Position: {player['final_position']} | Rating: {player['overall_rating']}, Training: {player['training_time']} hours\n"
        
        system_prompt += "\n"

    # Add optimized team context
    if team_data:
        system_prompt += f"""
CURRENTLY SELECTED 11 PLAYERS (Optimized Squad):
Formation: {team_data['formation']} (1 Goalkeeper - {team_data['formation']})
Total Players: {team_data['total_players']}
Total Team Rating: {team_data['total_rating']:.1f}
Total Training Time: {team_data['total_training_time']:.1f} hours
"""
        if team_data.get('max_training_time'):
            system_prompt += f"Max Training Time Constraint: {team_data['max_training_time']} hours\n"
        
        system_prompt += f"""Optimization Status: {team_data['status']}
Objective Value: {team_data['objective_value']:.2f}

Selected Players:
"""
        for player in team_data['players']:
            system_prompt += f"- {player['player_name']} ({player['team_name']}) - {player['assigned_role']} | Rating: {player['overall_rating']}, Training: {player['training_time']} hours\n"
        
        system_prompt += """
When discussing the team, you can refer to both the selected 11 players AND the complete roster. Provide tactical insights, suggest alternatives from the bench, analyze strengths and weaknesses.
"""
    
    system_prompt += "\nCurrent conversation context:"
    
    # Build conversation history
    conversation = system_prompt + "\n\n"
    for msg in chat_history[-6:]:
        conversation += f"{msg['role']}: {msg['content']}\n"
    conversation += f"User: {user_message}\nAssistant:"
    
    try:
        # Enable Google Search
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=conversation,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                response_modalities=["TEXT"]
            )
        )
        return response.text
    except Exception as e:
        return f"I apologize, but I encountered an error. Please try rephrasing your question. Error: {str(e)}"

# Callbacks
@app.callback(
    [Output('results-container', 'children'),
     Output('stats-container', 'children'),
     Output('optimality-container', 'children'),
     Output('selected-team-data', 'data'),
     Output('all-team-players-data', 'data')],
    Input('optimize-btn', 'n_clicks'),
    [State('team-id', 'value'),
     State('num-defenders', 'value'),
     State('num-midfielders', 'value'),
     State('num-forwards', 'value'),
     State('max-training-time', 'value')]
)
def optimize_team(n_clicks, team_id, num_defenders, num_midfielders, num_forwards, max_training_time):
    stats_display = html.Div()
    optimality_display = html.Div()
    team_data = None
    all_team_players_data = None
    
    if n_clicks is None or PLAYER_DATA is None:
        return html.Div([
            html.Div([
                html.H3("Ready to Build Your Squad", style={'color': '#2c3e50', 'fontWeight': '700', 'textAlign': 'center', 'marginTop': '100px'})
            ])
        ]), stats_display, optimality_display, team_data, all_team_players_data
    
    try:
        # Get ALL players from the selected team
        team_df = PLAYER_DATA[PLAYER_DATA["team_id"] == team_id]
        all_team_players_data = team_df[['player_name', 'team_name', 'final_position', 'overall_rating', 'training_time']].to_dict('records')
        
        result = run_optimization(PLAYER_DATA, team_id, num_defenders, num_midfielders, num_forwards, max_training_time)
        
        if result[0] is None:
            error_msg = result[1] if len(result) > 1 else "Optimization Failed"
            return html.Div([
                html.H3(error_msg, style={'color': '#e74c3c', 'textAlign': 'center'}),
                html.P("Try adjusting the formation or removing the training time constraint.", 
                       style={'textAlign': 'center', 'color': '#7f8c8d'})
            ]), stats_display, optimality_display, team_data, all_team_players_data
        
        selected_df, status, objective_value = result
        
        # Prepare team data for LLM
        team_data = {
            'players': selected_df.to_dict('records'),
            'total_players': len(selected_df),
            'total_rating': float(selected_df['overall_rating'].sum()),
            'total_training_time': float(selected_df['training_time'].sum()),
            'formation': f"{num_defenders}-{num_midfielders}-{num_forwards}",
            'status': status,
            'objective_value': float(objective_value),
            'max_training_time': max_training_time
        }

        # Stats cards
        stats_display = html.Div([
            html.Label("Squad Statistics", className="section-title"),
            html.Div([
                html.Div(len(selected_df), className='stat-value'),
                html.Div("Total Players", className='stat-label')
            ], className='stat-card'),
            html.Div([
                html.Div(f"{selected_df['overall_rating'].sum():.0f}", className='stat-value', style={'color': '#27ae60'}),
                html.Div("Total Rating", className='stat-label')
            ], className='stat-card'),
            html.Div([
                html.Div(f"{selected_df['training_time'].sum():.1f}", className='stat-value', style={'color': '#2c3e50'}),
                html.Div("Training Time (hrs)", className='stat-label')
            ], className='stat-card'),
        ])
        
        # Add training constraint status if applicable
        if max_training_time is not None and max_training_time > 0:
            constraint_met = selected_df['training_time'].sum() <= max_training_time
            stats_display.children.append(
                html.Div([
                    html.Div(f"{max_training_time}", className='stat-value', style={'color': '#27ae60' if constraint_met else '#e74c3c'}),
                    html.Div("Max Time Limit", className='stat-label')
                ], className='stat-card')
            )
        
        # Optimality check
        optimality_display = html.Div([
            html.Label("Optimization Status", className="section-title"),
            html.Div([
                html.Div([
                    html.Span("Status: ", style={'fontSize': '13px', 'color': '#7f8c8d', 'fontWeight': '600'}),
                    html.Span(status, className='badge-success' if status == 'Optimal' else 'badge-warning'),
                ], style={'marginBottom': '8px'}),
                html.Div([
                    html.Span("Objective: ", style={'fontSize': '12px', 'color': '#7f8c8d'}),
                    html.Span(f"{objective_value:.2f}", style={'fontSize': '12px', 'color': '#2c3e50', 'fontWeight': '700'})
                ])
            ], className='card-modern')
        ])
        
        # Main results
        results = html.Div([
            dbc.Row([
                # Left Column - Table and Chatbot
                dbc.Col([
                    # Player Table
                    html.Div([
                        html.Label("Selected Players", className="section-title"),
                        dash_table.DataTable(
                            data=selected_df[['player_name', 'team_name', 'assigned_role', 'overall_rating', 'training_time']].to_dict('records'),
                            columns=[
                                {'name': 'Player', 'id': 'player_name'},
                                {'name': 'Team', 'id': 'team_name'},
                                {'name': 'Role', 'id': 'assigned_role'},
                                {'name': 'Rating', 'id': 'overall_rating'},
                                {'name': 'Training (hrs)', 'id': 'training_time'}
                            ],
                            style_table={'overflowX': 'auto'},
                            style_cell={'textAlign': 'left', 'padding': '12px', 'fontSize': '13px', 'fontFamily': 'Inter, sans-serif', 'border': '1px solid #000000'},
                            style_header={'backgroundColor': 'white', 'fontWeight': '700', 'color': '#2c3e50', 'border': '1px solid #000000'},
                            style_data={'border': '1px solid #000000', 'backgroundColor': 'white'},
                            style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#f8f9fa'}]
                        )
                    ], className='card-modern'),
                    
                    # Chatbot
                    html.Div([
                        html.Label("Football Coach Assistant", className="section-title"),
                        
                        # Sample Prompts Section
                        html.Div([
                            html.Div([
                                html.Button("Analyze Squad", id='prompt-1', n_clicks=0, className='prompt-button'),
                                html.Button("Player Synergies", id='prompt-2', n_clicks=0, className='prompt-button'),
                                html.Button("Training Drill", id='prompt-3', n_clicks=0, className='prompt-button'),
                                html.Button("Match Strategy", id='prompt-4', n_clicks=0, className='prompt-button'),
                                html.Button("Roster Alternatives", id='prompt-5', n_clicks=0, className='prompt-button'),
                                html.Button("Tactical Adjustments", id='prompt-6', n_clicks=0, className='prompt-button'),
                            ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '4px', 'marginBottom': '12px'})
                        ], style={'marginBottom': '12px'}),
                        
                        html.Div([
                            html.Div(id='chat-messages', className='chat-messages'),
                            html.Div([
                                dbc.Input(id='chat-input', placeholder='Ask about tactics, players, formations...', className='input-modern', style={'flex': '1'}),
                                html.Button("Send", id='send-btn', className='btn-primary-modern', style={'padding': '10px 20px'})
                            ], className='chat-input-container')
                        ], className='chat-container')
                    ], className='card-modern')
                    
                ], width=7),
                
                # Right Column - Vertical Football Pitch
                dbc.Col([
                    html.Div([
                        html.Label("Team Formation", className="section-title"),
                        dcc.Graph(figure=create_vertical_pitch(selected_df), config={'displayModeBar': False}, style={'height': '950px'})
                    ], className='pitch-container')
                ], width=5)
            ])
        ])
        
        return results, stats_display, optimality_display, team_data, all_team_players_data
        
    except Exception as e:
        return html.Div([
            html.H3(f"Error: {str(e)}", style={'color': '#e74c3c', 'textAlign': 'center'})
        ]), stats_display, optimality_display, None, None

# Handle prompt button clicks
@app.callback(
    Output('chat-input', 'value', allow_duplicate=True),
    [Input('prompt-1', 'n_clicks'),
     Input('prompt-2', 'n_clicks'),
     Input('prompt-3', 'n_clicks'),
     Input('prompt-4', 'n_clicks'),
     Input('prompt-5', 'n_clicks'),
     Input('prompt-6', 'n_clicks')],
    prevent_initial_call=True
)
def fill_prompt(n1, n2, n3, n4, n5, n6):
    """Fill the input field with the selected prompt"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    prompts = {
        'prompt-1': "Analyze the tactical strengths and weaknesses of this optimized squad",
        'prompt-2': "Explain the player synergies and chemistry within the selected formation",
        'prompt-3': "Design a targeted training drill to improve our team's weakest areas",
        'prompt-4': "Create a match strategy that maximizes each player's individual strengths",
        'prompt-5': "Compare this squad to the complete roster - what are alternative lineup options?",
        'prompt-6': "What tactical adjustments should we make if we're losing at halftime?"
    }
    
    return prompts.get(button_id, "")

@app.callback(
    [Output('chat-messages', 'children'),
     Output('chat-history', 'data'),
     Output('chat-input', 'value', allow_duplicate=True)],
    Input('send-btn', 'n_clicks'),
    [State('chat-input', 'value'),
     State('chat-history', 'data'),
     State('selected-team-data', 'data'),
     State('all-team-players-data', 'data')],
    prevent_initial_call=True
)
def handle_chat(n_clicks, user_message, chat_history, team_data, all_team_players):
    if n_clicks is None or not user_message or user_message.strip() == '':
        if not chat_history:
            welcome_msg = "Hello! I'm your football coaching assistant with Google Search access. Ask me about tactics, formations, player strategies, or team analysis."
            if team_data:
                welcome_msg += f"\n\nI can see you've optimized a {team_data['formation']} formation. I also have access to all {len(all_team_players) if all_team_players else 0} players in your team roster!"
                if team_data.get('max_training_time'):
                    welcome_msg += f" Your training time constraint is {team_data['max_training_time']} hours."
            return [html.Div([
                dcc.Markdown(welcome_msg, style={'margin': '0'})
            ], className='chat-message bot-message')], chat_history, ''
        
        messages = []
        for msg in chat_history:
            if msg['role'] == 'user':
                messages.append(html.Div(msg['content'], className='chat-message user-message'))
            else:
                messages.append(html.Div([
                    dcc.Markdown(msg['content'], style={'margin': '0'})
                ], className='chat-message bot-message'))
        return messages, chat_history, ''
    
    chat_history.append({'role': 'user', 'content': user_message})
    
    # Get bot response with full context
    bot_response = get_football_assistant_response(user_message, chat_history, team_data, all_team_players)
    
    chat_history.append({'role': 'assistant', 'content': bot_response})
    
    messages = []
    for msg in chat_history:
        if msg['role'] == 'user':
            messages.append(html.Div(msg['content'], className='chat-message user-message'))
        else:
            messages.append(html.Div([
                dcc.Markdown(msg['content'], style={'margin': '0'})
            ], className='chat-message bot-message'))
    
    return messages, chat_history, ''

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)