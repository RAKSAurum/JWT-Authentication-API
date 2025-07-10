import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Create data structure for the treemap
data = []

# API Endpoints layer
api_endpoints = [
    "POST /login/",
    "POST /verify/", 
    "GET /validate/"
]

# Django Application layer
django_app = [
    "views.py",
    "utils.py", 
    "authentication.py",
    "settings.py"
]

# Infrastructure layer
infrastructure = [
    "Docker",
    "PostgreSQL",
    "AWS EC2",
    "Gunicorn"
]

# Security & Auth layer
security = [
    "PyJWT",
    "User Model",
    "Env Variables",
    "Auth Middleware"
]

# Create hierarchical data for treemap
for item in api_endpoints:
    data.append({
        'layer': 'API Endpoints',
        'component': item,
        'full_path': f"API Endpoints/{item}",
        'value': 1
    })

for item in django_app:
    data.append({
        'layer': 'Django App',
        'component': item,
        'full_path': f"Django App/{item}",
        'value': 1
    })

for item in infrastructure:
    data.append({
        'layer': 'Infrastructure',
        'component': item,
        'full_path': f"Infrastructure/{item}",
        'value': 1
    })

for item in security:
    data.append({
        'layer': 'Security & Auth',
        'component': item,
        'full_path': f"Security & Auth/{item}",
        'value': 1
    })

# Convert to DataFrame
df = pd.DataFrame(data)

# Create treemap
fig = px.treemap(
    df,
    path=['layer', 'component'],
    values='value',
    title='JWT Auth API Architecture',
    color='layer',
    color_discrete_sequence=['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F']
)

# Update layout for better visualization
fig.update_traces(
    textinfo="label",
    textfont_size=12,
    textfont_color='white',
    hovertemplate='<b>%{label}</b><br>Layer: %{parent}<extra></extra>'
)

fig.update_layout(
    font=dict(size=14),
    uniformtext_minsize=10,
    uniformtext_mode='hide'
)

# Save the chart
fig.write_image('jwt_auth_architecture.png')