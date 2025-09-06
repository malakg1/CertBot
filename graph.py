# graph_builder.py
from langgraph.graph import StateGraph, START, END
from state import State

# Import nodes (agents)
from gmail_utils import detect_certificates
from ocr_utils import extract_certificate_text
from enrichment import enrich_certificate_metadata
from linkedin import generate_linkedin_post, polish_post
from slack_utils import send_slack_preview
from linkedin_selenium import post_to_linkedin_selenium
from graphviz import Digraph
from langgraph.graph import START, END
from state import State


def build_graph():
    builder = StateGraph(State)
    builder.add_node("detect_certificates", detect_certificates)
    builder.add_node("extract_certificate_text", extract_certificate_text)
    builder.add_node("enrich_certificate_metadata", enrich_certificate_metadata)
    builder.add_node("generate_linkedin_post", generate_linkedin_post)
    builder.add_node("polish_post", polish_post)
    builder.add_node("send_slack_preview", send_slack_preview)
    builder.add_node("post_to_linkedin_selenium", post_to_linkedin_selenium)

    builder.add_edge(START, "detect_certificates")
    builder.add_edge("detect_certificates", "extract_certificate_text")
    builder.add_edge("extract_certificate_text", "enrich_certificate_metadata")
    builder.add_edge("enrich_certificate_metadata", "generate_linkedin_post")
    builder.add_edge("generate_linkedin_post", "polish_post")
    builder.add_edge("polish_post", "send_slack_preview")
    builder.add_edge("send_slack_preview", "post_to_linkedin_selenium")
    builder.add_edge("post_to_linkedin_selenium", END)

    return builder.compile()




def visualize_graph():
    builder = build_graph().builder  # uncompiled builder
    dot = Digraph(comment="Certificate Processing Graph", format='png')
    dot.attr(rankdir='TB')
    dot.attr('node', style='filled', fontname='Helvetica', fontsize='12')

    color_map = {
        "detect_certificates": "lightblue",
        "extract_certificate_text": "lightgreen",
        "enrich_certificate_metadata": "lightyellow",
        "generate_linkedin_post": "orange",
        "polish_post": "pink",
        "send_slack_preview": "violet",
        "post_to_linkedin_selenium": "lightcyan",
        START: "green",
        END: "red",
    }

    for node_name in builder.nodes:
        color = color_map.get(node_name, "white")
        shape = "oval" if node_name in [START, END] else "box"
        dot.node(node_name, label=node_name, shape=shape, fillcolor=color, style="filled,rounded")

    for src, dst in builder.edges:
        dot.edge(src, dst, color="gray")

    output_path = "state_graph_vertical"
    dot.render(output_path, view=True)
    print(f"Graph saved and rendered as {output_path}.png")
