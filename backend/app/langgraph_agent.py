import os
import re
import requests
from typing import Dict, Any
from .config import GROQ_API_KEY, GROQ_MODEL
import json

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

    def parse_transaction(self, prompt: str) -> Dict[str, Any]:
        """Ask the model to return a JSON object matching the HCP interaction schema.

        Falls back to structured local parsing when the model is not available or JSON parse fails.
        """
        if self.api_key:
            instruct = (
                "Return a JSON object with keys: hcp_name, interaction_type, date, time, attendees, "
                "topics, sentiment, outcomes, follow_up, notes, materials (list of {name}), samples (list of {name,quantity}). "
                f"Use the following content to extract fields: {prompt}"
            )
            response = self._call_groq(instruct)
            try:
                parsed = json.loads(response)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass

        return self._local_parse_transaction(prompt)

    def _local_parse_transaction(self, prompt: str) -> Dict[str, Any]:
        lower = prompt.lower()
        name = self._extract_hcp_name(prompt)
        sentiment = 'Positive' if any(word in lower for word in ['positive', 'promising', 'good', 'great', 'favorable', 'enthusiastic']) else 'Negative' if any(word in lower for word in ['negative', 'concern', 'issue', 'reject', 'not interested', 'no']) else 'Neutral'
        topics = self._extract_topics(prompt)
        outcomes = self._extract_outcomes(prompt)
        follow_up = self._extract_follow_up(prompt)
        return {
            'hcp_name': name,
            'interaction_type': 'Meeting',
            'date': '',
            'time': '',
            'attendees': '',
            'topics': topics,
            'sentiment': sentiment,
            'outcomes': outcomes,
            'follow_up': follow_up,
            'notes': prompt,
            'materials': [],
            'samples': [],
        }

    def _extract_hcp_name(self, prompt: str) -> str:
        patterns = [
            r'HCP\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            r'Dr\.\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            r'Dr\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            r'Mr\.\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            r'Ms\.\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            r'Mrs\.\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            r'with\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        ]
        for pattern in patterns:
            match = re.search(pattern, prompt)
            if match:
                return match.group(1).strip()
        return ''

    def _extract_topics(self, prompt: str) -> str:
        match = re.search(r'discussed\s+([^\.]+)', prompt, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        match = re.search(r'about\s+([^\.]+)', prompt, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return prompt

    def _extract_outcomes(self, prompt: str) -> str:
        match = re.search(r'resulted in\s+([^\.]+)', prompt, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        match = re.search(r'(the doctor|he|she) (responded|was|is) ([^\.]+)', prompt, re.IGNORECASE)
        if match:
            return match.group(0).strip()
        return ''

    def _extract_follow_up(self, prompt: str) -> str:
        match = re.search(r'follow[- ]?up[^\.]*', prompt, re.IGNORECASE)
        if match:
            return match.group(0).strip()
        match = re.search(r'next\s+(steps|meeting|action|visit)[^\.]*', prompt, re.IGNORECASE)
        if match:
            return match.group(0).strip()
        return ''

    def route_tool(self, prompt: str) -> str:
        lowered = prompt.lower()
        if any(keyword in lowered for keyword in ['log', 'transaction', 'record']):
            return 'Log Interaction'
        if 'follow-up' in lowered or 'follow up' in lowered or 'next step' in lowered:
            return 'Follow-up Planner'
        if 'sentiment' in lowered:
            return 'Sentiment Classifier'
        if 'summarize' in lowered:
            return 'Summarize Interaction'
        return 'AI Assistant'

    def tool_list(self) -> Dict[str, str]:
        return {
            'Log Interaction': 'Capture structured HCP interaction details and store them securely.',
            'Edit Interaction': 'Modify any saved interaction fields or updates to notes, materials, and samples.',
            'Summarize Interaction': 'Generate concise AI summaries and sales highlight notes.',
            'Follow-up Planner': 'Extract follow-up actions, next steps, and suggested customer outreach.',
            'Sentiment Classifier': 'Infer expected HCP sentiment from interaction content for prioritization.',
        }
