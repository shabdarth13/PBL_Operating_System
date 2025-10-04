import re
import json
import platform
import logging
import difflib

logger = logging.getLogger(__name__)

class NLPCommandParser:
    def __init__(self, config_path=None):
        self.is_windows = platform.system() == "Windows"
        self.command_mappings = self._load_command_mappings(config_path)
        self.filler_words = [
            "please", "can you", "could you", "would you", "will you",
            "i want to", "i would like to", "kindly", "just"
        ]
    def _load_command_mappings(self, config_path=None):
        if config_path:
            with open(config_path, 'r') as f:
                data = json.load(f)
                return data.get("command_mappings", {})
        return {}
    def _normalize_input(self, text: str) -> str:
        text = text.lower().strip()
        for filler in self.filler_words:
            text = text.replace(filler, "")
        return text.strip()
    def _fuzzy_match(self, input_text: str, patterns: list[str], threshold: float = 0.7):
        """Return the first regex pattern that matches or is similar to input_text"""
        for pat in patterns:
            if re.search(pat, input_text):
                return pat
            ratio = difflib.SequenceMatcher(None, input_text, pat).ratio()
            if ratio >= threshold:
                return pat
        return None

    def _extract_parameters(self, pattern: str, text: str, command_template: str):
        """
        Extract parameters from regex match and map them to placeholders in the command template.
        Supports multiple parameters in any order.
        """
        match = re.search(pattern, text)
        if not match:
            return {}

        groups = match.groups()
        placeholders = re.findall(r"\{(\w+)\}", command_template)
        params = {}

        for i, g in enumerate(groups):
            if i < len(placeholders):
                params[placeholders[i]] = g.strip()
            else:
                params[f"param{i+1}"] = g.strip()
        return params

    def parse_command(self, text: str):
        original_text = text
        text = self._normalize_input(text)

        for category, mapping in self.command_mappings.items():
            patterns = mapping.get("patterns", [])
            matched_pattern = self._fuzzy_match(text, patterns)
            if matched_pattern:
                command_template = (
                    mapping["windows_command"] if self.is_windows
                    else mapping.get("linux_command", mapping["windows_command"])
                )
                params = self._extract_parameters(matched_pattern, text, command_template)
                required_placeholders = re.findall(r"\{(\w+)\}", command_template)
                missing = [ph for ph in required_placeholders if ph not in params or not params[ph]]
                if missing:
                    return None, params, f"Missing parameters: {', '.join(missing)}", {
                        "category": category,
                        "dangerous": mapping.get("dangerous", False),
                        "description": mapping.get("description", ""),
                        "missing": missing
                    }

                try:
                    command = command_template.format(**params)
                except KeyError:
                    command = command_template
                metadata = {
                    "category": category,
                    "dangerous": mapping.get("dangerous", False),
                    "description": mapping.get("description", "")
                }
                return command, params, mapping.get("description", ""), metadata
        return text, {}, "Direct execution", {"category": "direct", "dangerous": False}
