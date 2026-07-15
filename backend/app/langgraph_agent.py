import os
import requests
from typing import Dict, Any
from .config import GROQ_API_KEY, GROQ_MODEL

GROQ_ENDPOINT = 'https://api.groq.com/v1/generate'

class LangGraphAgent:
    """Simulated LangGraph-style agent for HCP interaction tools."""

    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.model = GROQ_MODEL

    def _local_summary(self, prompt: str) -> str:
        return (
            "This interaction log describes a meeting with an HCP. Key points: "
            "topics covered, sentiment observed, materials and sample details, and follow-up actions. "
            "The record can be saved or edited for compliance and sales tracking."
        )

    def _call_groq(self, prompt: str) -> str:
        if not self.api_key:
            return self._local_summary(prompt)

        payload = {
            'model': self.model,
            'prompt': prompt,
            'max_output_tokens': 300,
            'temperature': 0.2,
        }
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        response = requests.post(GROQ_ENDPOINT, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data.get('text', self._local_summary(prompt)).strip()

    def summarize_interaction(self, interaction: Dict[str, Any]) -> str:
        prompt = (
            f"Summarize this HCP interaction in a concise professional sales note. "
            f"HCP: {interaction.get('hcp_name')}. Type: {interaction.get('interaction_type')}. "
            f"Topics: {interaction.get('topics')}. Attendees: {interaction.get('attendees')}. "
            f"Outcomes: {interaction.get('outcomes')}. Follow-up: {interaction.get('follow_up')}. "
            f"Sentiment: {interaction.get('sentiment')}."
        )
        return self._call_groq(prompt)

    def extract_action_items(self, notes: str) -> str:
        prompt = (
            f"Extract follow-up actions, suggested next steps, and any sales opportunities from this interaction note: {notes}"
        )
        return self._call_groq(prompt)

    def classify_sentiment(self, topics: str) -> str:
        prompt = f"Classify the sentiment of this interaction as positive, neutral, or negative: {topics}"
        return self._call_groq(prompt)

    def help_describe(self, description: str) -> str:
        prompt = f"Provide a clear assistant blurb for the following interaction description: {description}"
        return self._call_groq(prompt)

    def tool_list(self) -> Dict[str, str]:
        return {
            'Log Interaction': 'Capture structured HCP interaction details and store them securely.',
            'Edit Interaction': 'Modify any saved interaction fields or updates to notes, materials, and samples.',
            'Summarize Interaction': 'Generate concise AI summaries and sales highlight notes.',
            'Follow-up Planner': 'Extract follow-up actions, next steps, and suggested customer outreach.',
            'Sentiment Classifier': 'Infer expected HCP sentiment from interaction content for prioritization.',
        }
