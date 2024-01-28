import plotly.graph_objects as go
import pandas as pd

structure = "FCC"
df_sqs_2 = pd.read_excel("bokas.xlsx", sheet_name="Structure")
# df_sqs_2 = pd.read_excel('./enthalpy_data_and_predictions/pairwise_mixing_enthalpy.xlsx', sheet_name="our work")
df_sqs_2.set_index('Unnamed: 0', inplace=True)


pa.Hea(structure, df_sqs_2)
# Generate some sample data
temperature = [100, 150, 200, 250, 300, 350, 400]  # Temperature values
energy_above_hull = [5, 4.5, 4, 3.8, 4.2, 5, 6]  # Energy above hull values

# Create a line plot
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=temperature,
    y=energy_above_hull,
    mode='lines',
    line=dict(
        color='blue',
    ),
))

# Add a phase change point with a label
phase_change_temp = 275
phase_change_energy = 3.5
fig.add_trace(go.Scatter(
    x=[phase_change_temp],
    y=[phase_change_energy],
    mode='markers',
    marker=dict(
        size=10,
        color='red',
        symbol='x',
    ),
    text='Phase Change',
    textposition='top center',
))

# Set the layout and labels
fig.update_layout(
    title='Temperature vs Energy Above Hull',
    xaxis_title='Temperature (°C)',
    yaxis_title='Energy Above Hull',
)

# Show the graph
fig.show()