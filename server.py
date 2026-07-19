import os
import json
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse, FileResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from agent.ai_agent import AIAgent
from agent.runtime import LANForgeRuntime
from agent.lanforge_executor import RuntimeInventoryAdapter
from agent.execution_pipeline import ExecutionPipeline
from agent.conversation_manager import ConversationManager

# Initialize the AI Agent
agent = AIAgent()

async def get_status(request):
    runtime = agent.executor.runtime
    connected = False
    host = None
    inventory = {
        "stations": [],
        "ethernet": [],
        "radios": []
    }
    
    if runtime and runtime.connected:
        connected = True
        host = runtime.host
        inventory = {
            "stations": sorted(list(runtime.stations.keys())),
            "ethernet": sorted(list(runtime.ethernet.keys())),
            "radios": sorted(list(runtime.radios.keys()))
        }
        
    return JSONResponse({
        "connected": connected,
        "host": host,
        "inventory": inventory
    })

async def connect_lanforge(request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"status": "error", "message": "Invalid JSON request body"}, status_code=400)
        
    host = body.get("host")
    if not host:
        return JSONResponse({"status": "error", "message": "LANForge Host IP is required"}, status_code=400)
        
    try:
        # Perform connection
        agent.executor.connect(host)
        runtime = agent.executor.runtime
        if runtime and runtime.connected:
            return JSONResponse({
                "status": "success",
                "message": f"Connected to LANForge Manager at {host}",
                "host": host,
                "inventory": {
                    "stations": sorted(list(runtime.stations.keys())),
                    "ethernet": sorted(list(runtime.ethernet.keys())),
                    "radios": sorted(list(runtime.radios.keys()))
                }
            })
        else:
            return JSONResponse({
                "status": "error",
                "message": f"Connection check failed for IP {host}. Verify it is active."
            }, status_code=500)
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": f"Failed to connect: {str(e)}"
        }, status_code=500)

async def query_intent(request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"status": "error", "message": "Invalid JSON request body"}, status_code=400)
        
    question = body.get("question")
    if not question:
        return JSONResponse({"status": "error", "message": "Query question is required"}, status_code=400)
        
    # Check if LANForge is connected
    runtime = agent.executor.runtime
    if not runtime or not runtime.connected:
        return JSONResponse({
            "status": "error",
            "message": "LANForge is not connected. Please connect first."
        }, status_code=400)
        
    try:
        # Extract initial values and resolve script
        values = agent.executor.parameter_extractor.extract(question)
        result = agent.executor.script_resolver.resolve(question)
        
        script = result.get("script")
        if not script:
            return JSONResponse({
                "status": "error",
                "message": "No matching LANForge script could be found for your request.",
                "reason": result.get("reason", "No matching script.")
            }, status_code=404)
            
        # Build script execution schema
        execution = agent.executor._build_execution(script)
        
        # Run preparation pipeline
        pipeline_result = agent.executor.pipeline.prepare(script, execution, values)
        
        # Build dynamic argument mapping
        arguments = []
        for dest, arg in execution["info"].items():
            resolver = arg.get("resolver")
            if not resolver:
                if dest in ["station", "stations"]:
                    resolver = "stations"
                elif dest in ["upstream", "upstream_port", "upstream_ports"]:
                    resolver = "ethernet"
                elif dest in ["radio", "radios"]:
                    resolver = "radios"

            choices = arg.get("choices")
            options = []
            
            # Fetch options from active inventory resolver
            if resolver:
                options = sorted(list(getattr(agent.executor.runtime_view, resolver, {}).keys()))
            elif choices:
                options = choices
                
            arguments.append({
                "name": dest,
                "help": arg.get("help", ""),
                "default": arg.get("default", ""),
                "required": dest in execution["required"],
                "multiple": arg.get("multiple", False),
                "options": options,
                "friendly_name": arg.get("friendly_name", dest),
                "group": arg.get("group", "Advanced"),
                "placeholder": arg.get("placeholder", "")
            })
            
        return JSONResponse({
            "status": "success",
            "script": script,
            "confidence": result.get("confidence", 0.0),
            "reason": result.get("reason", ""),
            "required": execution["required"],
            "optional": execution["optional"],
            "arguments": arguments,
            "extracted_values": values,
            "auto_resolved": pipeline_result.get("known", {}),
            "missing": pipeline_result.get("missing", [])
        })
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": f"Query processing failed: {str(e)}"
        }, status_code=500)

async def execute_script(request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"status": "error", "message": "Invalid JSON request body"}, status_code=400)
        
    script = body.get("script")
    parameters = body.get("parameters", {})
    
    if not script:
        return JSONResponse({"status": "error", "message": "Script name is required"}, status_code=400)
        
    runtime = agent.executor.runtime
    if not runtime or not runtime.connected:
        return JSONResponse({"status": "error", "message": "LANForge is not connected."}, status_code=400)
        
    try:
        execution = agent.executor._build_execution(script)
        pipeline_result = agent.executor.pipeline.prepare(script, execution, parameters)
        
        if pipeline_result["status"] == "missing":
            return JSONResponse({
                "status": "error",
                "message": "Missing required parameters",
                "missing": pipeline_result["missing"]
            }, status_code=400)
            
        # Execute the built script command on LANForge via SSH
        cmd_result = agent.executor.ssh.execute(pipeline_result["command"])
        
        return JSONResponse({
            "status": "completed",
            "command": pipeline_result["command"],
            "stdout": cmd_result.get("stdout", ""),
            "stderr": cmd_result.get("stderr", "")
        })
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": f"Execution failed: {str(e)}"
        }, status_code=500)

routes = [
    Route("/api/status", get_status, methods=["GET"]),
    Route("/api/connect", connect_lanforge, methods=["POST"]),
    Route("/api/query", query_intent, methods=["POST"]),
    Route("/api/execute", execute_script, methods=["POST"]),
]

# If Vite build exists, serve it
if os.path.exists("dist"):
    routes.append(Mount("/assets", StaticFiles(directory="dist/assets"), name="assets"))
    async def serve_index(request):
        return FileResponse("dist/index.html")
    routes.append(Route("/", serve_index, methods=["GET"]))

middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
]

app = Starlette(routes=routes, middleware=middleware)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
