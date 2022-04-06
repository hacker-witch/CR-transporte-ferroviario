import pandas as pd
import networkx as nx
import plotly.graph_objects as go

edges_df = pd.read_excel('todas-as-linhas/arestas.xlsx')

G = nx.from_pandas_edgelist(edges_df, 'Source', 'Target')

closeness_dict = nx.closeness_centrality(G)
betweenness_dict = nx.betweenness_centrality(G)
position_dict = nx.kamada_kawai_layout(G)

nx.set_node_attributes(G, position_dict, 'position')
nx.set_node_attributes(G, betweenness_dict, 'betweenness')
nx.set_node_attributes(G, closeness_dict, 'closeness')

node_trace = go.Scatter(
  x = [],
  y = [],
  text = [],
  textposition='top center',
  mode='markers+text',
  marker=dict(
    showscale=True,
    colorscale='YlGnBu',
    color=[],
    size=10,
    colorbar=dict(
      thickness=15,
      title='Centralidade de Intermediação',
      xanchor='left',
      titleside='right'
    ),
    line_width=2
  )
)

for node_id in G.nodes():
  node = G.nodes[node_id]
  
  x, y = node['position']
  node_trace['x'] += tuple([x])
  node_trace['y'] += tuple([y])

  node_trace['text'] += tuple([f'<b>{node_id}</b>'])

node_trace.marker.color = list(betweenness_dict.values())

edges_x = []
edges_y = []
for edge in G.edges():
  source_id, target_id = edge

  source = G.nodes()[source_id]
  target = G.nodes()[target_id]

  source_x, source_y = source['position']
  target_x, target_y = target['position']

  edges_x.append(source_x)
  edges_x.append(target_x)
  edges_x.append(None)
  
  edges_y.append(source_y)
  edges_y.append(target_y)
  edges_y.append(None)

edge_trace = go.Scatter(
    x=edges_x, y=edges_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

layout = go.Layout(
  showlegend=False,
  hovermode='closest',
  margin=dict(b=20,l=5,r=5,t=40),
  xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
  yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
)

fig = go.Figure(layout=layout)

fig.add_trace(edge_trace)
fig.add_trace(node_trace)

fig.show()