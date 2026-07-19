import os
import re
import json
import logging
from ollama import Client

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Constants
DEFAULT_SCRIPTS_PATHS = [
    r"C:\Users\Amaresh.Koti\Documents\lanforge-scripts",
    r"C:\Users\Amaresh.Koti\Downloads\lanforge-scripts-master\lanforge-scripts-master",
]
KNOWLEDGE_FILE = "knowledge/knowledge.json"
OLLAMA_MODEL = "gpt-oss:20b"


class MultipleValueScanner:
    def __init__(self, scripts_dir=None, ollama_host=None):
        # Resolve script directory path
        self.scripts_dir = None
        if scripts_dir:
            self.scripts_dir = scripts_dir
        else:
            for path in DEFAULT_SCRIPTS_PATHS:
                if os.path.exists(path):
                    self.scripts_dir = path
                    break
        
        # If still not found, check current directory files
        if not self.scripts_dir:
            self.scripts_dir = "."
            
        logger.info(f"Using scripts repository directory: {self.scripts_dir}")
        
        # Configure Ollama Client
        if not ollama_host:
            try:
                from config import OLLAMA_HOST
                ollama_host = OLLAMA_HOST
            except ImportError:
                ollama_host = "http://localhost:11434"
                
        logger.info(f"Connecting to Ollama at: {ollama_host}")
        self.client = Client(host=ollama_host)
        
    def _extract_argparse_block(self, file_path):
        """Extract argparse add_argument statements to keep prompt size tiny."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Could not read file {file_path}: {e}")
            return ""

        # Extract lines that contain argument declarations
        lines = content.splitlines()
        argparse_lines = []
        capture = False
        bracket_count = 0
        
        for line in lines:
            # Detect starting pattern of argument addition
            if "add_argument" in line:
                capture = True
                
            if capture:
                argparse_lines.append(line)
                bracket_count += line.count("(") - line.count(")")
                if bracket_count <= 0:
                    capture = False
                    bracket_count = 0
                    
        return "\n".join(argparse_lines)

    def scan_script(self, file_path):
        """Pass argparse definitions to Ollama and get rich parameters mapping."""
        extracted_code = self._extract_argparse_block(file_path)
        if not extracted_code.strip():
            return []

        prompt = f"""
You are an expert LANforge test configuration parser.
Analyze the following python argument parser code block.

Argument Parser Code:
{extracted_code}

For each argument, extract:
1. "dest": the parameter destination/variable name (e.g., "upstream", "stations", "dut", "traffic_types")
2. "multiple": true if the argument accepts multiple comma-separated values, lists of values, or is list-compatible. Otherwise false.
3. "resolver": set to one of the following strings if it maps to active LANforge resource lists:
   - "stations" (if it specifies station/client interfaces, e.g. wlan0, sta0000)
   - "ethernet" (if it specifies ethernet/upstream ports, e.g. eth0, eth1, enp0s3)
   - "radios" (if it specifies radio interfaces, e.g. wiphy0, wiphy1)
   - "ssids" (if it specifies Wi-Fi SSID network names)
   - "bssid" (if it specifies BSSID MAC addresses)
   - null (for everything else)
4. "friendly_name": a clear, user-friendly readable label for the field in the UI.
5. "group": categorize the field as one of: "Networking", "Traffic", "Wireless", "Reporting", "Advanced".
6. "placeholder": a helpful placeholder showing a sample value (e.g. "1.1.eth1" for ports, "1.10.wlan0" for stations, "linksys-8450" for DUT, "UDP,TCP" for traffic types).

Return ONLY a valid JSON list of objects. No explanation, no markdown tags.

Example output:
[
  {{
    "dest": "upstream",
    "multiple": false,
    "resolver": "ethernet",
    "friendly_name": "Upstream Port",
    "group": "Networking",
    "placeholder": "1.1.eth1"
  }},
  {{
    "dest": "traffic_types",
    "multiple": true,
    "resolver": null,
    "friendly_name": "Traffic Types",
    "group": "Traffic",
    "placeholder": "UDP,TCP"
  }}
]
"""
        try:
            response = self.client.chat(
                model=OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response["message"]["content"].strip()
            
            # Strip potential code fence blocks
            if content.startswith("```"):
                lines = content.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                content = "\n".join(lines).strip()
                
            param_list = json.loads(content)
            if isinstance(param_list, list):
                return param_list
            return []
        except Exception as e:
            logger.error(f"Error querying Ollama for {os.path.basename(file_path)}: {e}")
            return []

    def update_knowledge_base(self):
        """Scan entire repository and update knowledge/knowledge.json."""
        if not os.path.exists(KNOWLEDGE_FILE):
            logger.error(f"Knowledge file {KNOWLEDGE_FILE} does not exist!")
            return False

        try:
            with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                knowledge = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load knowledge database: {e}")
            return False

        scripts = list(knowledge.get("scripts", {}).keys())
        logger.info(f"Scanning scripts listed in knowledge base: {len(scripts)} scripts found.")

        # Find exact files in scripts repository
        script_files = {}
        for root, _, files in os.walk(self.scripts_dir):
            for file in files:
                if file.endswith(".py"):
                    script_files[file] = os.path.join(root, file)

        updated_count = 0
        for script_name in scripts:
            file_path = script_files.get(script_name)
            if not file_path:
                logger.warning(f"Could not find local file for script: {script_name}")
                continue

            logger.info(f"Analyzing multi-value and metadata properties for script: {script_name}...")
            enriched_params = self.scan_script(file_path)
            
            if enriched_params:
                logger.info(f"Script {script_name} enriched parameters: {len(enriched_params)} found.")
                
                # Update knowledge model mapping
                for arg in knowledge["scripts"][script_name].get("arguments", []):
                    dest = arg.get("dest")
                    name = arg.get("name")
                    
                    # Find matching enriched definition
                    enrich_def = next((x for x in enriched_params if x.get("dest") == dest or x.get("dest") == name or (arg.get("aliases") and any(a.replace("-", "") == x.get("dest") for a in arg.get("aliases")))), None)
                    if enrich_def:
                        arg["multiple"] = enrich_def.get("multiple", False)
                        arg["resolver"] = enrich_def.get("resolver")
                        
                        # Set optional metadata fields
                        if "friendly_name" in enrich_def:
                            arg["friendly_name"] = enrich_def["friendly_name"]
                        if "group" in enrich_def:
                            arg["group"] = enrich_def["group"]
                        if "placeholder" in enrich_def:
                            arg["placeholder"] = enrich_def["placeholder"]
                            
                        updated_count += 1
            else:
                logger.info(f"No custom parameter metadata extracted for {script_name}")

        # Write back updated knowledge json file
        try:
            with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
                json.dump(knowledge, f, indent=2, ensure_ascii=False)
            logger.info(f"Successfully updated knowledge.json. Saved {updated_count} enriched parameter definitions.")
            return True
        except Exception as e:
            logger.error(f"Failed to write updated knowledge file: {e}")
            return False


if __name__ == "__main__":
    scanner = MultipleValueScanner()
    scanner.update_knowledge_base()
