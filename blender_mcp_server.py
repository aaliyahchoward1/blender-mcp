#!/usr/bin/env python3
"""
Blender MCP Bridge Server

Provides Model Context Protocol interface to Blender model generators.
Run this server on your machine where Blender is installed, then connect
Claude Code to it via MCP configuration.

Usage:
    python3 blender_mcp_server.py [--port 5555]

Then in Claude Code settings.json:
    {
      "mcpServers": {
        "blender": {
          "command": "python3",
          "args": ["/path/to/blender_mcp_server.py"],
          "env": {"BLENDER_PATH": "/path/to/blender"}
        }
      }
    }
"""

import json
import sys
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Any, Dict, Optional

# MCP Protocol helpers
class MCPServer:
    def __init__(self):
        self.blender_path = os.environ.get("BLENDER_PATH", "blender")
        self.models_dir = Path(__file__).parent / "models"

    def read_request(self) -> Dict[str, Any]:
        """Read JSON-RPC request from stdin."""
        try:
            line = input()
            return json.loads(line)
        except EOFError:
            return None

    def send_response(self, request_id: Optional[str], result: Any = None, error: Optional[str] = None):
        """Send JSON-RPC response to stdout."""
        response = {"jsonrpc": "2.0"}
        if request_id:
            response["id"] = request_id
        if error:
            response["error"] = {"code": -1, "message": error}
        else:
            response["result"] = result
        print(json.dumps(response), flush=True)

    def run_blender_script(self, script_content: str) -> tuple[bool, str]:
        """Execute Python script in Blender and return output."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(script_content)
                script_path = f.name

            try:
                result = subprocess.run(
                    [self.blender_path, "-b", "-P", script_path],
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                if result.returncode == 0:
                    return True, result.stdout
                else:
                    return False, result.stderr
            finally:
                os.unlink(script_path)

        except FileNotFoundError:
            return False, f"Blender not found at: {self.blender_path}"
        except subprocess.TimeoutExpired:
            return False, "Blender script execution timed out (60s)"
        except Exception as e:
            return False, f"Error running Blender: {str(e)}"

    def generate_lunuff(self, options: Dict = None) -> Dict[str, Any]:
        """Generate Lunuff character."""
        options = options or {}
        scale = options.get("scale", 1.0)

        script = f'''
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "models"))

from lunuff_character import LunuffModelGenerator

gen = LunuffModelGenerator()
model = gen.generate()

# Apply scale if specified
if {scale} != 1.0:
    model.scale = ({scale}, {scale}, {scale})
    import bpy
    bpy.ops.object.transform_apply(scale=True)

# Export
gen.export_stl(model)

print(f"SUCCESS: Generated Lunuff - {{model.name}}")
print(f"Vertices: {{len(model.data.vertices)}}")
print(f"Faces: {{len(model.data.polygons)}}")
'''

        success, output = self.run_blender_script(script)

        return {
            "success": success,
            "message": output,
            "type": "lunuff_character"
        }

    def generate_from_text_to_cad(self, description: str, options: Dict = None) -> Dict[str, Any]:
        """Generate model from text description."""
        options = options or {}

        # Escape quotes in description
        description = description.replace('"', '\\"')

        script = f'''
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "models"))

from text_to_cad_integration import TextToCADGenerator

gen = TextToCADGenerator()
obj = gen.generate_from_description("{description}")
export_path = gen.export_stl(obj)

print(f"SUCCESS: Generated CAD model - {{obj.name}}")
print(f"Description: {description}")
print(f"Vertices: {{len(obj.data.vertices)}}")
print(f"Faces: {{len(obj.data.polygons)}}")
print(f"Export: {{export_path}}")
'''

        success, output = self.run_blender_script(script)

        return {
            "success": success,
            "message": output,
            "description": description,
            "type": "text_to_cad"
        }

    def generate_unified(self, request: str, options: Dict = None) -> Dict[str, Any]:
        """Generate using unified router."""
        options = options or {}

        # Escape quotes in request
        request = request.replace('"', '\\"')

        script = f'''
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "models"))

from unified_model_generator import UnifiedModelGenerator

gen = UnifiedModelGenerator()

# Route the request
routing = gen.route_request("{request}")
print(f"ROUTING: {{routing['tool']}}")
print(f"REASONING: {{routing['reasoning']}}")

# Generate
result = gen.generate("{request}")

if result["status"] == "success":
    print(f"SUCCESS: {{result['tool']}} generator")
    for key, value in result.items():
        if key != "status":
            print(f"{{key}}: {{value}}")
else:
    print(f"ERROR: {{result.get('message', 'Unknown error')}}")
'''

        success, output = self.run_blender_script(script)

        return {
            "success": success,
            "message": output,
            "request": request,
            "type": "unified"
        }

    def get_tools(self) -> list:
        """Return available MCP tools."""
        return [
            {
                "name": "generate_lunuff",
                "description": "Generate a complete Lunuff character model",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "scale": {
                            "type": "number",
                            "description": "Scale multiplier (default 1.0)"
                        }
                    }
                }
            },
            {
                "name": "generate_text_to_cad",
                "description": "Generate 3D model from text description",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "description": {
                            "type": "string",
                            "description": "Natural language description of the model to generate"
                        }
                    },
                    "required": ["description"]
                }
            },
            {
                "name": "generate_unified",
                "description": "Generate using intelligent router (Lunuff or Text-to-CAD)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "request": {
                            "type": "string",
                            "description": "Natural language request - router picks the right tool"
                        }
                    },
                    "required": ["request"]
                }
            }
        ]

    def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle JSON-RPC request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            if method == "initialize":
                response = {
                    "capabilities": {
                        "tools": self.get_tools()
                    }
                }
                self.send_response(request_id, response)

            elif method == "tools/list":
                self.send_response(request_id, {"tools": self.get_tools()})

            elif method == "tools/call":
                tool_name = params.get("name")
                tool_input = params.get("arguments", {})

                if tool_name == "generate_lunuff":
                    result = self.generate_lunuff(tool_input)
                elif tool_name == "generate_text_to_cad":
                    result = self.generate_text_to_cad(
                        tool_input.get("description", ""),
                        tool_input
                    )
                elif tool_name == "generate_unified":
                    result = self.generate_unified(
                        tool_input.get("request", ""),
                        tool_input
                    )
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}

                self.send_response(request_id, result)
            else:
                self.send_response(request_id, error=f"Unknown method: {method}")

        except Exception as e:
            self.send_response(request_id, error=f"Error: {str(e)}")

    def run(self):
        """Main server loop."""
        print("Blender MCP Server started", file=sys.stderr)
        print(f"Blender path: {self.blender_path}", file=sys.stderr)
        print(f"Models directory: {self.models_dir}", file=sys.stderr)

        while True:
            try:
                request = self.read_request()
                if request is None:
                    break
                self.handle_request(request)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Server error: {e}", file=sys.stderr)


if __name__ == "__main__":
    server = MCPServer()
    server.run()
