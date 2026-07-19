import React, { useState, useEffect, useRef } from "react";
import Hls from "hls.js";
import { motion, AnimatePresence } from "framer-motion";
import {
  Network,
  Globe,
  ArrowRight,
  Check,
  Search,
  Terminal,
  Activity,
  Cpu,
  FolderOpen,
  AlertCircle,
  X,
  Loader2,
  ChevronDown,
  Play,
  Send
} from "lucide-react";

// HLS Background Video Player
const BackgroundVideo = () => {
  const videoRef = useRef(null);
  const streamUrl = "https://stream.mux.com/kimF2ha9zLrX64H00UgLGPflCzNtl1T0215MlAmeOztv8.m3u8";

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    if (video.canPlayType("application/vnd.apple.mpegurl")) {
      video.src = streamUrl;
    } else if (Hls.isSupported()) {
      const hls = new Hls();
      hls.loadSource(streamUrl);
      hls.attachMedia(video);
      return () => {
        hls.destroy();
      };
    }
  }, []);

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
      <video
        ref={videoRef}
        autoPlay
        muted
        loop
        playsInline
        className="w-full h-full object-cover opacity-30 transition-opacity duration-1000"
      />
      <div className="absolute inset-0 bg-gradient-to-t from-black via-black/80 to-black/40" />
    </div>
  );
};

const NetworkNocWorkspace = ({ smoothX, smoothY }) => {
  const canvasBaseRef = useRef(null);
  const canvasRevealRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    const canvasBase = canvasBaseRef.current;
    const canvasReveal = canvasRevealRef.current;
    if (!canvasBase || !canvasReveal) return;

    const ctxBase = canvasBase.getContext("2d");
    const ctxReveal = canvasReveal.getContext("2d");

    let animationFrame;
    let width = 0;
    let height = 0;

    const rawNodes = [
      { id: 0, name: "LANForge Manager", xPct: 0.18, yPct: 0.28, type: "manager", status: "online", speed: "1 Gbps" },
      { id: 1, name: "NOC Core Switch", xPct: 0.38, yPct: 0.16, type: "switch", status: "online", speed: "10 Gbps" },
      { id: 2, name: "NOC Core Router", xPct: 0.58, yPct: 0.24, type: "router", status: "online", speed: "40 Gbps" },
      { id: 3, name: "WiFi 7 AP", xPct: 0.14, yPct: 0.52, type: "ap", status: "online", speed: "9.8 Gbps" },
      { id: 4, name: "WiFi 6E AP", xPct: 0.86, yPct: 0.52, type: "ap", status: "online", speed: "4.8 Gbps" },
      { id: 5, name: "Test Chamber A", xPct: 0.36, yPct: 0.80, type: "chamber", status: "busy", speed: "2.4 Gbps" },
      { id: 6, name: "Test Chamber B", xPct: 0.64, yPct: 0.80, type: "chamber", status: "online", speed: "2.4 Gbps" },
      { id: 7, name: "Station sta0001", xPct: 0.28, yPct: 0.88, type: "client", status: "online", speed: "866 Mbps" },
      { id: 8, name: "Station sta0002", xPct: 0.44, yPct: 0.88, type: "client", status: "online", speed: "1.2 Gbps" },
      { id: 9, name: "Laptop client", xPct: 0.08, yPct: 0.38, type: "client", status: "online", speed: "600 Mbps" },
      { id: 10, name: "Phone client", xPct: 0.22, yPct: 0.42, type: "client", status: "online", speed: "433 Mbps" },
      { id: 11, name: "IoT Device", xPct: 0.92, yPct: 0.38, type: "client", status: "online", speed: "50 Mbps" }
    ];

    const rawLinks = [
      { from: 0, to: 1, phase: 0.0 },
      { from: 1, to: 2, phase: 0.25 },
      { from: 2, to: 3, phase: 0.5 },
      { from: 2, to: 4, phase: 0.75 },
      { from: 2, to: 5, phase: 0.1 },
      { from: 2, to: 6, phase: 0.6 },
      { from: 3, to: 9, phase: 0.3 },
      { from: 3, to: 10, phase: 0.8 },
      { from: 4, to: 11, phase: 0.2 },
      { from: 5, to: 7, phase: 0.4 },
      { from: 5, to: 8, phase: 0.9 }
    ];

    const resize = () => {
      const parent = containerRef.current;
      if (!parent) return;
      width = parent.clientWidth;
      height = parent.clientHeight;
      canvasBase.width = width;
      canvasBase.height = height;
      canvasReveal.width = width;
      canvasReveal.height = height;
    };

    window.addEventListener("resize", resize);
    resize();

    const draw = () => {
      ctxBase.clearRect(0, 0, width, height);
      ctxReveal.clearRect(0, 0, width, height);

      const nodes = rawNodes.map(n => ({
        ...n,
        x: n.xPct * width,
        y: n.yPct * height
      }));

      const t = Date.now() / 1000;

      // Draw Base Layer
      ctxBase.lineWidth = 1.5;
      ctxBase.strokeStyle = "rgba(255, 255, 255, 0.05)";
      rawLinks.forEach(link => {
        const fromNode = nodes[link.from];
        const toNode = nodes[link.to];
        ctxBase.beginPath();
        ctxBase.moveTo(fromNode.x, fromNode.y);
        ctxBase.lineTo(toNode.x, toNode.y);
        ctxBase.stroke();
      });

      nodes.forEach(node => {
        ctxBase.fillStyle = "rgba(100, 116, 139, 0.15)";
        ctxBase.strokeStyle = "rgba(255, 255, 255, 0.1)";
        ctxBase.lineWidth = 1;
        ctxBase.beginPath();
        ctxBase.arc(node.x, node.y, 6, 0, Math.PI * 2);
        ctxBase.fill();
        ctxBase.stroke();

        ctxBase.fillStyle = "rgba(255, 255, 255, 0.15)";
        ctxBase.font = "9px Inter";
        ctxBase.textAlign = "center";
        ctxBase.fillText(node.name, node.x, node.y - 12);
      });

      // Draw Reveal Layer
      rawLinks.forEach(link => {
        const fromNode = nodes[link.from];
        const toNode = nodes[link.to];
        
        const grad = ctxReveal.createLinearGradient(fromNode.x, fromNode.y, toNode.x, toNode.y);
        grad.addColorStop(0, "rgba(59, 130, 246, 0.3)");
        grad.addColorStop(1, "rgba(0, 212, 255, 0.3)");

        ctxReveal.lineWidth = 1.8;
        ctxReveal.strokeStyle = grad;
        ctxReveal.beginPath();
        ctxReveal.moveTo(fromNode.x, fromNode.y);
        ctxReveal.lineTo(toNode.x, toNode.y);
        ctxReveal.stroke();

        const speedFactor = 0.45;
        const pos = (t * speedFactor + link.phase) % 1.0;
        const px = fromNode.x + (toNode.x - fromNode.x) * pos;
        const py = fromNode.y + (toNode.y - fromNode.y) * pos;

        ctxReveal.fillStyle = "#00D4FF";
        ctxReveal.shadowBlur = 6;
        ctxReveal.shadowColor = "#00D4FF";
        ctxReveal.beginPath();
        ctxReveal.arc(px, py, 3, 0, Math.PI * 2);
        ctxReveal.fill();
        ctxReveal.shadowBlur = 0;
      });

      [3, 4].forEach(apId => {
        const apNode = nodes[apId];
        if (apNode) {
          const waveRadius = ((Date.now() / 20) % 130) + 10;
          const alpha = 1.0 - waveRadius / 130;
          ctxReveal.strokeStyle = `rgba(0, 212, 255, ${alpha * 0.2})`;
          ctxReveal.lineWidth = 1.0;
          ctxReveal.beginPath();
          ctxReveal.arc(apNode.x, apNode.y, waveRadius, 0, Math.PI * 2);
          ctxReveal.stroke();
        }
      });

      nodes.forEach(node => {
        const pulse = Math.sin(t * 4 + node.id) * 0.12 + 1.0;
        ctxReveal.fillStyle = node.status === "busy" ? "rgba(239, 68, 68, 0.15)" : "rgba(16, 185, 129, 0.15)";
        ctxReveal.strokeStyle = node.status === "busy" ? "rgba(239, 68, 68, 0.7)" : "rgba(0, 212, 255, 0.7)";
        ctxReveal.lineWidth = 1.2;

        ctxReveal.beginPath();
        ctxReveal.arc(node.x, node.y, 6.5 * pulse, 0, Math.PI * 2);
        ctxReveal.fill();
        ctxReveal.stroke();

        ctxReveal.fillStyle = node.status === "busy" ? "#EF4444" : "#10B981";
        ctxReveal.beginPath();
        ctxReveal.arc(node.x, node.y, 2.5, 0, Math.PI * 2);
        ctxReveal.fill();

        ctxReveal.fillStyle = "#ffffff";
        ctxReveal.font = "500 9px Inter";
        ctxReveal.textAlign = "center";
        ctxReveal.fillText(node.name, node.x, node.y - 12);

        ctxReveal.fillStyle = "rgba(0, 212, 255, 0.85)";
        ctxReveal.font = "400 8px Inter";
        ctxReveal.fillText(node.speed, node.x, node.y + 15);
      });

      animationFrame = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      window.removeEventListener("resize", resize);
      cancelAnimationFrame(animationFrame);
    };
  }, []);

  return (
    <div ref={containerRef} className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
      <canvas ref={canvasBaseRef} className="absolute inset-0 block w-full h-full opacity-50" />
      <div
        style={{
          position: "absolute",
          inset: 0,
          maskImage: `radial-gradient(circle 260px at ${smoothX}px ${smoothY}px, black 60%, transparent 100%)`,
          WebkitMaskImage: `radial-gradient(circle 260px at ${smoothX}px ${smoothY}px, black 60%, transparent 100%)`
        }}
      >
        <canvas ref={canvasRevealRef} className="absolute inset-0 block w-full h-full" />
      </div>
    </div>
  );
};

const CustomSelect = ({ label, options, value, onChange, multiple, placeholder }) => {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef(null);

  // Close dropdown on click outside
  useEffect(() => {
    const handleOutsideClick = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleOutsideClick);
    return () => document.removeEventListener("mousedown", handleOutsideClick);
  }, []);

  const selectedValues = multiple
    ? (value ? value.split(",").filter(Boolean) : [])
    : (value ? [value] : []);

  const handleOptionClick = (opt) => {
    if (multiple) {
      let nextValues;
      if (selectedValues.includes(opt)) {
        nextValues = selectedValues.filter(v => v !== opt);
      } else {
        nextValues = [...selectedValues, opt];
      }
      onChange(nextValues.join(","));
    } else {
      onChange(opt);
      setIsOpen(false);
    }
  };

  return (
    <div ref={containerRef} className="relative w-full">
      <div
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-white text-sm outline-none focus:border-white/30 flex items-center justify-between cursor-pointer hover:bg-white/[0.08] transition-all duration-200"
      >
        <span className={selectedValues.length === 0 ? "text-white/30 text-xs italic" : "text-white text-sm"}>
          {selectedValues.length > 0
            ? (multiple ? selectedValues.join(", ") : selectedValues[0])
            : (placeholder || "-- Select Option --")}
        </span>
        <ChevronDown className={`w-4 h-4 text-white/40 transition-transform duration-200 ${isOpen ? "rotate-180" : ""}`} />
      </div>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -4 }}
            transition={{ duration: 0.15 }}
            className="absolute z-50 left-0 right-0 mt-1 max-h-48 overflow-y-auto bg-black/95 border border-white/15 rounded-lg shadow-2xl backdrop-blur-md"
          >
            {options.length === 0 ? (
              <div className="px-3 py-2 text-xs text-white/40 italic">No options available</div>
            ) : (
              options.map((opt) => {
                const isSelected = selectedValues.includes(opt);
                return (
                  <div
                    key={opt}
                    onClick={() => handleOptionClick(opt)}
                    className="flex items-center justify-between px-3 py-2 text-sm hover:bg-white/10 cursor-pointer transition-colors duration-150"
                  >
                    <span className={isSelected ? "text-emerald-400 font-medium" : "text-white/80"}>
                      {opt}
                    </span>
                    {isSelected && <Check className="w-4 h-4 text-emerald-400" />}
                  </div>
                );
              })
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const ChatMessage = ({ msg, onAnswerSubmit, isActiveStep }) => {
  const [selectedRadio, setSelectedRadio] = useState("");
  const [selectedChecks, setSelectedChecks] = useState([]);
  const [inputText, setInputText] = useState("");
  const [selectedOptionalParams, setSelectedOptionalParams] = useState([]);

  const isAi = msg.sender === "ai";

  const handleControlSubmit = () => {
    if (msg.controlType === "radio") {
      onAnswerSubmit(selectedRadio);
    } else if (msg.controlType === "checkbox") {
      onAnswerSubmit(selectedChecks.join(","));
    } else if (msg.controlType === "text") {
      onAnswerSubmit(inputText);
    } else if (msg.controlType === "optional_confirm") {
      onAnswerSubmit(inputText);
    } else if (msg.controlType === "optional_select") {
      onAnswerSubmit(selectedOptionalParams);
    }
  };

  return (
    <div className={`flex flex-col gap-1.5 ${isAi ? "items-start" : "items-end"}`}>
      {/* Sender Label */}
      <span className="text-[10px] text-white/40 px-3 uppercase tracking-wider font-mono">
        {isAi ? "AI Assistant" : "User"}
      </span>
      
      {/* Message Card */}
      <div className={`max-w-[85%] rounded-2xl p-4 border text-sm relative ${
        isAi 
          ? "bg-white/5 border-white/10 text-white/90 rounded-tl-sm" 
          : "bg-emerald-500/10 border-emerald-500/20 text-emerald-300 rounded-tr-sm"
      }`}>
        <p className="whitespace-pre-wrap leading-relaxed">
          {msg.text}
          {isAi && msg.required && <span className="text-rose-500 font-bold ml-1">*</span>}
        </p>

        {/* Help Text */}
        {isAi && msg.help && (
          <p className="text-[10px] text-white/40 mt-1 border-t border-white/5 pt-1 italic">
            {msg.help}
          </p>
        )}

        {/* Dynamic Controls */}
        {isAi && msg.controlType && isActiveStep && (
          <div className="mt-4 pt-3 border-t border-white/10 flex flex-col gap-3">
            {msg.controlType === "radio" && (
              <div className="flex flex-col gap-2 max-h-40 overflow-y-auto pr-1">
                {msg.options.map((opt) => (
                  <label key={opt} className="flex items-center gap-2 cursor-pointer text-xs text-white/80 hover:text-white">
                    <input
                      type="radio"
                      name={msg.paramName}
                      value={opt}
                      checked={selectedRadio === opt}
                      onChange={() => setSelectedRadio(opt)}
                      className="accent-emerald-400"
                    />
                    <span>{opt}</span>
                  </label>
                ))}
              </div>
            )}

            {msg.controlType === "checkbox" && (
              <div className="flex flex-col gap-2 max-h-40 overflow-y-auto pr-1">
                {msg.options.map((opt) => (
                  <label key={opt} className="flex items-center gap-2 cursor-pointer text-xs text-white/80 hover:text-white">
                    <input
                      type="checkbox"
                      value={opt}
                      checked={selectedChecks.includes(opt)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedChecks([...selectedChecks, opt]);
                        } else {
                          setSelectedChecks(selectedChecks.filter(c => c !== opt));
                        }
                      }}
                      className="accent-emerald-400 rounded"
                    />
                    <span>{opt}</span>
                  </label>
                ))}
              </div>
            )}

            {msg.controlType === "text" && (
              <input
                type="text"
                placeholder={msg.placeholder || "Enter value..."}
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleControlSubmit()}
                className="w-full px-3 py-1.5 bg-black/40 border border-white/10 rounded-lg text-white text-xs outline-none focus:border-white/30"
              />
            )}

            {msg.controlType === "optional_confirm" && (
              <div className="flex gap-2">
                <button
                  onClick={() => onAnswerSubmit("yes")}
                  className="px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium hover:bg-emerald-500/20 transition-colors cursor-pointer flex-1"
                >
                  Yes, configure optional params
                </button>
                <button
                  onClick={() => onAnswerSubmit("no")}
                  className="px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 text-white text-xs font-medium hover:bg-white/10 transition-colors cursor-pointer flex-1"
                >
                  No, execute script now
                </button>
              </div>
            )}

            {msg.controlType === "optional_select" && (
              <div className="flex flex-col gap-3">
                <div className="flex flex-col gap-2 max-h-40 overflow-y-auto pr-1">
                  {msg.options.map((opt) => (
                    <label key={opt} className="flex items-center gap-2 cursor-pointer text-xs text-white/80 hover:text-white">
                      <input
                        type="checkbox"
                        value={opt}
                        checked={selectedOptionalParams.includes(opt)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setSelectedOptionalParams([...selectedOptionalParams, opt]);
                          } else {
                            setSelectedOptionalParams(selectedOptionalParams.filter(c => c !== opt));
                          }
                        }}
                        className="accent-emerald-400 rounded"
                      />
                      <span>{opt}</span>
                    </label>
                  ))}
                </div>
                <div className="flex gap-2 border-t border-white/5 pt-2">
                  <button
                    onClick={() => onAnswerSubmit(selectedOptionalParams)}
                    className="px-3 py-1.5 rounded-lg bg-emerald-500 text-black text-xs font-semibold hover:bg-emerald-400 transition-colors cursor-pointer flex-1"
                  >
                    Configure Selected ({selectedOptionalParams.length})
                  </button>
                  <button
                    onClick={() => onAnswerSubmit([])}
                    className="px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 text-white text-xs font-medium hover:bg-white/10 transition-colors cursor-pointer flex-1"
                  >
                    Skip Optional & Run
                  </button>
                </div>
              </div>
            )}

            {msg.controlType !== "optional_confirm" && msg.controlType !== "optional_select" && (
              <div className="flex justify-end mt-1">
                <button
                  onClick={handleControlSubmit}
                  className="px-4 py-1.5 bg-emerald-500 text-black font-semibold text-xs rounded-lg hover:bg-emerald-400 transition-colors cursor-pointer"
                >
                  Submit
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default function App() {
  // Navigation & Landing Page States
  const [email, setEmail] = useState("");
  const [emailSubmitted, setEmailSubmitted] = useState(false);
  const [showEmailForm, setShowEmailForm] = useState(false);
  const emailTimerRef = useRef(null);

  // Overlay / Workspace States
  const [showConsole, setShowConsole] = useState(false);

  // Mouse tracking states for NOC spotlight reveal
  const [mouse, setMouse] = useState({ x: -1000, y: -1000 });
  const smoothMouse = useRef({ x: 0, y: 0 });
  const [smoothPos, setSmoothPos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMouse({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  useEffect(() => {
    let animFrame;
    const updateSmooth = () => {
      const dx = mouse.x - smoothMouse.current.x;
      const dy = mouse.y - smoothMouse.current.y;
      smoothMouse.current.x += dx * 0.08; // smooth easing
      smoothMouse.current.y += dy * 0.08;
      setSmoothPos({ x: smoothMouse.current.x, y: smoothMouse.current.y });
      animFrame = requestAnimationFrame(updateSmooth);
    };
    animFrame = requestAnimationFrame(updateSmooth);
    return () => cancelAnimationFrame(animFrame);
  }, [mouse]);
  
  // LANForge Connection States
  const [lanforgeIp, setLanforgeIp] = useState("192.168.244.97");
  const [isConnected, setIsConnected] = useState(false);
  const [isVerified, setIsVerified] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [connectError, setConnectError] = useState("");
  const [inventory, setInventory] = useState({ stations: [], ethernet: [], radios: [] });

  // Query & Script Parameters
  const [searchQuery, setSearchQuery] = useState("");
  const [isQuerying, setIsQuerying] = useState(false);
  const [queryResult, setQueryResult] = useState(null);
  const [queryError, setQueryError] = useState("");

  // Parameters Form States
  const [formParams, setFormParams] = useState({});
  const [showAdvanced, setShowAdvanced] = useState(false);

  // Test Run Execution
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState(null);
  const [executionError, setExecutionError] = useState("");
  const [executedCommand, setExecutedCommand] = useState("");
  const [terminalLines, setTerminalLines] = useState([]);

  // Chat/Interview States
  const [chatMessages, setChatMessages] = useState([
    { id: "1", sender: "ai", text: "LANForge AI Console Workspace active. Enter a script request like 'run dataplane test' or type a command." }
  ]);
  const [chatInput, setChatInput] = useState("");
  const [chatState, setChatState] = useState("idle"); // "idle", "collecting_required", "optional_confirm", "optional_select", "optional_input", "ready"
  const [missingRequired, setMissingRequired] = useState([]);
  const [currentStep, setCurrentStep] = useState(0);
  const [pendingOptional, setPendingOptional] = useState([]);
  const [optionalStep, setOptionalStep] = useState(0);

  const messagesEndRef = useRef(null);

  // Auto-scroll messages list
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  // Check connection status on load
  useEffect(() => {
    fetch("/api/status")
      .then((res) => res.json())
      .then((data) => {
        if (data.connected) {
          setIsConnected(true);
          setLanforgeIp(data.host);
          setInventory(data.inventory);
        }
      })
      .catch((err) => console.error("Failed to check status", err));
  }, []);

  // Handle landing page demo early access toggle
  const handleLaunchConsoleClick = () => {
    if (isConnected) {
      setShowConsole(true);
    } else {
      setShowEmailForm(true);
      if (emailTimerRef.current) clearTimeout(emailTimerRef.current);
      emailTimerRef.current = setTimeout(() => {
        setShowEmailForm(false);
        setEmailSubmitted(false);
      }, 4000);
    }
  };

  const handleEmailSubmit = (e) => {
    e.preventDefault();
    if (!email) return;
    setEmailSubmitted(true);
    if (emailTimerRef.current) clearTimeout(emailTimerRef.current);
    emailTimerRef.current = setTimeout(() => {
      setShowEmailForm(false);
      setEmailSubmitted(false);
      setEmail("");
      // Force open Console to allow connection
      setShowConsole(true);
    }, 2000);
  };

  // Perform LANForge connection
  const handleConnect = async (e) => {
    e?.preventDefault();
    if (!lanforgeIp) return;
    setIsConnecting(true);
    setConnectError("");

    try {
      const res = await fetch("/api/connect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ host: lanforgeIp })
      });
      const data = await res.json();
      if (res.ok && data.status === "success") {
        setInventory(data.inventory);
        setIsVerified(true);
      } else {
        setConnectError(data.message || "Failed to establish connection.");
      }
    } catch (err) {
      setConnectError("Network error. Make sure the LANForge server is running.");
    } finally {
      setIsConnecting(false);
    }
  };

  // Run natural language script resolver
  const handleSearchSubmit = async (e) => {
    e.preventDefault();
    if (!searchQuery) return;
    setIsQuerying(true);
    setQueryError("");
    setQueryResult(null);
    setExecutionResult(null);
    setExecutionError(null);

    try {
      const res = await fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: searchQuery })
      });
      const data = await res.json();
      if (res.ok && data.status === "success") {
        setQueryResult(data);
        
        // Initialize form parameters from extracted and auto-resolved values
        const initialParams = {};
        data.arguments.forEach(arg => {
          initialParams[arg.name] = data.extracted_values[arg.name] || data.auto_resolved[arg.name] || arg.default || "";
        });
        setFormParams(initialParams);
      } else {
        setQueryError(data.message || "No script resolved for query.");
      }
    } catch (err) {
      setQueryError("Query resolution request failed.");
    } finally {
      setIsQuerying(false);
    }
  };

  // Run test script execution on LANForge
  const handleExecute = async (overrideParams = null) => {
    if (!queryResult) return;
    setIsExecuting(true);
    setChatState("executing");
    setExecutionError("");
    setExecutionResult(null);
    setExecutedCommand("");

    const activeParams = overrideParams || formParams;
    const approxCmd = `python3 ${queryResult.script} ` + Object.entries(activeParams)
      .filter(([_, val]) => val !== "" && val !== null && val !== undefined)
      .map(([key, val]) => `--${key} "${val}"`)
      .join(" ");

    setTerminalLines([
      { type: "system", text: `[system] Establishing SSH connection to admin@${lanforgeIp}...` },
      { type: "system", text: `[system] Authentication successful (port 22).` },
      { type: "command", text: `$ ${approxCmd}` }
    ]);

    setChatMessages((prev) => [
      ...prev,
      {
        id: Date.now() + "-ai-run-start",
        sender: "ai",
        text: "Executing script automation on LANForge SSH server. Please monitor logs in the terminal."
      }
    ]);

    const simulatedLogs = [
      `[${queryResult.script}] Initializing connection to LANForge Manager on port 8080...`,
      `[${queryResult.script}] Loading automation libraries...`,
      `[${queryResult.script}] Discovering active port layouts, radios, and stations...`,
      `[${queryResult.script}] Verifying execution environment locks...`,
      `[${queryResult.script}] Active test run launched. Duration set to ${activeParams.duration || "10"} seconds...`,
      `[${queryResult.script}] Injecting active traffic streams...`,
      `[${queryResult.script}] Reading interface throughput stats...`,
      `[${queryResult.script}] Validating transmission packet counters...`
    ];

    let step = 0;
    const logInterval = setInterval(() => {
      if (step < simulatedLogs.length) {
        setTerminalLines((prev) => [
          ...prev,
          { type: "log", text: simulatedLogs[step] }
        ]);
        step++;
      }
    }, 1200);

    try {
      const res = await fetch("/api/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          script: queryResult.script,
          parameters: activeParams
        })
      });
      const data = await res.json();
      clearInterval(logInterval);

      if (res.ok) {
        setExecutionResult(data);
        if (data.command) {
          setExecutedCommand(data.command);
        }
        setTerminalLines((prev) => [
          ...prev,
          { type: "system", text: `\n[system] Command Execution Completed (Status: Success)` },
          { type: "command_actual", text: `Executed Command:\n${data.command}` },
          ...(data.stdout ? [{ type: "stdout", text: data.stdout }] : []),
          ...(data.stderr ? [{ type: "stderr", text: data.stderr }] : [])
        ]);
        setChatMessages((prev) => [
          ...prev,
          {
            id: Date.now() + "-ai-run-end-ok",
            sender: "ai",
            text: "Script automation completed successfully!"
          }
        ]);
      } else {
        setExecutionError(data.message || "Execution script failed.");
        setTerminalLines((prev) => [
          ...prev,
          { type: "error", text: `\n[system] Command Execution Failed: ${data.message || "Unknown error"}` },
          ...(data.stderr ? [{ type: "stderr", text: data.stderr }] : [])
        ]);
        setChatMessages((prev) => [
          ...prev,
          {
            id: Date.now() + "-ai-run-end-err",
            sender: "ai",
            text: `Execution failed: ${data.message}`
          }
        ]);
      }
    } catch (err) {
      clearInterval(logInterval);
      setExecutionError("Execution request timed out or was aborted.");
      setTerminalLines((prev) => [
        ...prev,
        { type: "error", text: `\n[system] Command Execution Error: Connection timed out or was aborted.` }
      ]);
      setChatMessages((prev) => [
        ...prev,
        {
          id: Date.now() + "-ai-run-end-net",
          sender: "ai",
          text: `Connection failed: ${err.message}`
        }
      ]);
    } finally {
      setIsExecuting(false);
      setChatState("idle");
    }
  };

  const askParameter = (paramName, state, dataContext = null) => {
    const context = dataContext || queryResult;
    if (!context) return;

    const argument = context.arguments.find(arg => arg.name === paramName);
    if (!argument) {
      setChatMessages((prev) => [
        ...prev,
        {
          id: Date.now() + "-ai-missing-arg-" + paramName,
          sender: "ai",
          text: `Please enter a value for '${paramName}':`,
          controlType: "text",
          paramName,
          required: state === "collecting_required"
        }
      ]);
      return;
    }

    const isRequired = state === "collecting_required";
    const displayLabel = argument.friendly_name || argument.name;
    let text = isRequired 
      ? `Please provide a value for '${displayLabel}':`
      : `Provide optional value for '${displayLabel}':`;

    if (argument.name === "upstream") {
      text = "Which upstream Ethernet port should I use?";
    } else if (argument.name === "station" || argument.name === "stations") {
      text = "Which station should I use?";
    } else if (argument.name === "dut") {
      text = "What device under test (DUT) should I use?";
    } else if (argument.name === "traffic_types") {
      text = "What traffic types should I use?";
    } else if (argument.name === "traffic_directions") {
      text = "Which traffic directions should I use?";
    } else if (argument.help) {
      text = argument.help;
    }

    setChatMessages((prev) => [
      ...prev,
      {
        id: Date.now() + "-ai-arg-" + paramName,
        sender: "ai",
        text,
        help: argument.help !== text ? argument.help : undefined,
        controlType: argument.options && argument.options.length > 0 
          ? (argument.multiple ? "checkbox" : "radio") 
          : "text",
        options: argument.options,
        multiple: argument.multiple,
        paramName,
        required: isRequired,
        placeholder: argument.placeholder || (argument.default ? `Default: ${argument.default}` : "Enter value...")
      }
    ]);
  };

  const handleChatAnswerSubmit = (answer) => {
    const userText = Array.isArray(answer)
      ? (answer.length > 0 ? `Selected options: ${answer.join(", ")}` : "Skip optional parameter configuration")
      : (answer === "" ? "Keep default" : String(answer));

    setChatMessages((prev) => [
      ...prev,
      { id: Date.now() + "-user-ans", sender: "user", text: userText }
    ]);

    if (chatState === "collecting_required") {
      const activeParam = missingRequired[currentStep];
      const nextParams = { ...formParams, [activeParam]: answer };
      setFormParams(nextParams);

      const nextStep = currentStep + 1;
      if (nextStep < missingRequired.length) {
        setCurrentStep(nextStep);
        askParameter(missingRequired[nextStep], "collecting_required");
      } else {
        setChatState("optional_confirm");
        setChatMessages((prev) => [
          ...prev,
          {
            id: Date.now() + "-ai-confirm",
            sender: "ai",
            text: "Required parameters collected. Would you like to configure optional parameters?",
            controlType: "optional_confirm"
          }
        ]);
      }
    } else if (chatState === "optional_confirm") {
      if (answer === "yes") {
        setChatState("optional_select");
        setChatMessages((prev) => [
          ...prev,
          {
            id: Date.now() + "-ai-select",
            sender: "ai",
            text: "Select which optional parameters you would like to configure:",
            controlType: "optional_select",
            options: queryResult.optional
          }
        ]);
      } else {
        handleExecute();
      }
    } else if (chatState === "optional_select") {
      if (answer && answer.length > 0) {
        setPendingOptional(answer);
        setOptionalStep(0);
        setChatState("optional_input");
        askParameter(answer[0], "optional_input");
      } else {
        handleExecute();
      }
    } else if (chatState === "optional_input") {
      const activeParam = pendingOptional[optionalStep];
      const nextParams = { ...formParams, [activeParam]: answer };
      setFormParams(nextParams);

      const nextOptionalStep = optionalStep + 1;
      if (nextOptionalStep < pendingOptional.length) {
        setOptionalStep(nextOptionalStep);
        askParameter(pendingOptional[nextOptionalStep], "optional_input");
      } else {
        handleExecute(nextParams);
      }
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const text = chatInput;
    setChatInput("");
    setChatMessages((prev) => [
      ...prev,
      { id: Date.now() + "-user-input", sender: "user", text }
    ]);

    if (chatState === "collecting_required" || chatState === "optional_input") {
      handleChatAnswerSubmit(text);
      return;
    }

    setIsQuerying(true);
    setQueryResult(null);
    setFormParams({});
    setExecutedCommand("");
    setExecutionResult(null);
    setExecutionError(null);
    setQueryError("");

    try {
      const res = await fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text })
      });
      const data = await res.json();

      if (res.ok) {
        setQueryResult(data);
        const initialParams = { ...data.extracted_values, ...data.auto_resolved };
        setFormParams(initialParams);

        const missing = data.required.filter(p => !initialParams[p] || initialParams[p] === "");

        setChatMessages((prev) => [
          ...prev,
          {
            id: Date.now() + "-ai-resolved",
            sender: "ai",
            text: `Matched script: ${data.script}\n\n${data.reason}`
          }
        ]);

        if (missing.length > 0) {
          setChatState("collecting_required");
          setMissingRequired(missing);
          setCurrentStep(0);
          setTimeout(() => {
            askParameter(missing[0], "collecting_required", data);
          }, 300);
        } else {
          setChatState("optional_confirm");
          setTimeout(() => {
            setChatMessages((prev) => [
              ...prev,
              {
                id: Date.now() + "-ai-confirm",
                sender: "ai",
                text: "Required parameters collected. Would you like to configure optional parameters?",
                controlType: "optional_confirm"
              }
            ]);
          }, 300);
        }
      } else {
        setChatMessages((prev) => [
          ...prev,
          {
            id: Date.now() + "-ai-query-err",
            sender: "ai",
            text: `Query processing failed: ${data.message || "No script resolved."}`
          }
        ]);
      }
    } catch (err) {
      setChatMessages((prev) => [
        ...prev,
        {
          id: Date.now() + "-ai-query-err-net",
          sender: "ai",
          text: `Network request error: ${err.message}`
        }
      ]);
    } finally {
      setIsQuerying(false);
    }
  };

  return (
    <main className="relative bg-black h-screen w-screen flex flex-col overflow-hidden selection:bg-white selection:text-black shrink-0 text-white font-sans">
      {!isConnected ? (
        // ==========================================
        // 1. STUNNING LOGIN PAGE (FORMER LANDING PAGE STYLE)
        // ==========================================
        <>
          <NetworkNocWorkspace smoothX={smoothPos.x} smoothY={smoothPos.y} />

          {/* Floating Enterprise Cards */}
          <div className="absolute inset-0 pointer-events-none z-10 hidden md:block overflow-hidden">
            {/* Card 1: AI Command */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.5 }}
              className="absolute left-[8%] top-[25%]"
            >
              <motion.div
                animate={{ y: [0, -8, 0] }}
                transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
                className="w-[260px] p-4 bg-white/5 border border-white/10 rounded-xl backdrop-blur-md shadow-2xl"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] text-white/40 uppercase font-mono tracking-wider">AI Command</span>
                  <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[9px] font-mono font-medium">
                    Workflow Ready
                  </span>
                </div>
                <p className="text-xs text-white/80 leading-relaxed font-light">
                  "Run a dataplane test on all WiFi 7 stations for 10 minutes."
                </p>
              </motion.div>
            </motion.div>

            {/* Card 2: Inventory (Loads only when verified!) */}
            {isVerified && (
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                className="absolute left-[6%] top-[55%]"
              >
                <motion.div
                  animate={{ y: [0, -12, 0] }}
                  transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
                  className="w-[200px] p-4 bg-white/5 border border-white/10 rounded-xl backdrop-blur-md shadow-2xl animate-fade-in"
                >
                  <span className="text-[10px] text-white/40 uppercase font-mono tracking-wider block mb-3">Inventory</span>
                  <div className="grid grid-cols-2 gap-y-2.5 gap-x-2 text-xs">
                    <div>
                      <span className="text-white/40 block text-[9px]">Stations</span>
                      <span className="text-sm font-semibold text-white">{inventory?.stations?.length || 0}</span>
                    </div>
                    <div>
                      <span className="text-white/40 block text-[9px]">Radios</span>
                      <span className="text-sm font-semibold text-white">{inventory?.radios?.length || 0}</span>
                    </div>
                    <div>
                      <span className="text-white/40 block text-[9px]">Ethernet</span>
                      <span className="text-sm font-semibold text-white">{inventory?.ethernet?.length || 0}</span>
                    </div>
                    <div>
                      <span className="text-white/40 block text-[9px]">Resources</span>
                      <span className="text-sm font-semibold text-cyan-400">
                        {(inventory?.stations?.length || 0) + (inventory?.radios?.length || 0) + (inventory?.ethernet?.length || 0)}
                      </span>
                    </div>
                  </div>
                </motion.div>
              </motion.div>
            )}

            {/* Card 3: Execution Checklist */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="absolute right-[8%] top-[20%]"
            >
              <motion.div
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 5.5, repeat: Infinity, ease: "easeInOut" }}
                className="w-[240px] p-4 bg-white/5 border border-white/10 rounded-xl backdrop-blur-md shadow-2xl"
              >
                <span className="text-[10px] text-white/40 uppercase font-mono tracking-wider block mb-3">Workflow Execution</span>
                <div className="space-y-2 text-[11px] font-light">
                  <div className="flex items-center gap-2 text-white/50">
                    <span className="w-3.5 h-3.5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-[9px] font-bold">✓</span>
                    <span>Discovering Inventory</span>
                  </div>
                  <div className="flex items-center gap-2 text-white/50">
                    <span className="w-3.5 h-3.5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-[9px] font-bold">✓</span>
                    <span>Selecting Stations</span>
                  </div>
                  <div className="flex items-center gap-2 text-white/50">
                    <span className="w-3.5 h-3.5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-[9px] font-bold">✓</span>
                    <span>Generating Workflow</span>
                  </div>
                  <div className="flex items-center gap-2 text-cyan-400">
                    <span className="w-3.5 h-3.5 rounded-full bg-cyan-500/20 border border-cyan-400/30 flex items-center justify-center text-[9px] animate-pulse">●</span>
                    <span className="font-medium">Running Test</span>
                  </div>
                  <div className="flex items-center gap-2 text-white/30">
                    <span className="w-3.5 h-3.5 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-[9px]">-</span>
                    <span>Generating Report</span>
                  </div>
                </div>
              </motion.div>
            </motion.div>

            {/* Card 4: Network Health */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.8 }}
              className="absolute right-[6%] top-[58%]"
            >
              <motion.div
                animate={{ y: [0, -7, 0] }}
                transition={{ duration: 6.5, repeat: Infinity, ease: "easeInOut" }}
                className="w-[220px] p-4 bg-white/5 border border-white/10 rounded-xl backdrop-blur-md shadow-2xl"
              >
                <span className="text-[10px] text-white/40 uppercase font-mono tracking-wider block mb-3">Live Telemetry</span>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-white/40">Latency:</span>
                    <span className="text-white font-medium">2.1 ms</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/40">Packet Loss:</span>
                    <span className="text-white font-medium">0.00%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/40">Throughput:</span>
                    <span className="text-emerald-400 font-semibold">9.8 Gbps</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-white/40">Signal Quality:</span>
                    <span className="px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[9px] font-mono">
                      Excellent
                    </span>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          </div>

          {/* HERO SECTION / CENTERED LOGIN CARD */}
          <div className="relative flex-1 flex flex-col items-center justify-center px-6 pt-12 pb-8 min-h-0">
            <div className="relative z-10 text-center max-w-5xl mx-auto flex flex-col items-center justify-center w-full gap-6 my-auto">
              <motion.p
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="text-white/60 text-[10px] md:text-[11px] font-semibold tracking-[0.25em] uppercase"
              >
                AI-POWERED NETWORK TEST AUTOMATION
              </motion.p>

              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
                className="text-4xl md:text-[54px] font-bold tracking-tight leading-[1.15] text-white max-w-4xl"
              >
                Control Your <br />
                <span style={{ fontFamily: "'Playfair Display', Georgia, serif" }} className="italic font-normal text-cyan-400">LANForge</span> Lab With <span style={{ fontFamily: "'Playfair Display', Georgia, serif" }} className="italic font-normal text-blue-400">AI</span>
              </motion.h1>

              {/* Login Form */}
              <motion.div
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="w-full max-w-md bg-white/[0.03] border border-white/10 rounded-2xl p-6 backdrop-blur-md shadow-2xl flex flex-col gap-4 mt-4"
              >
                <div className="text-left">
                  <label className="block text-[10px] font-semibold text-white/40 uppercase tracking-wider mb-2 font-mono flex items-center justify-between">
                    <span>LANForge Manager IP Address</span>
                    {isVerified && <span className="text-emerald-400 font-bold font-sans">✓ Verified</span>}
                  </label>
                  <input
                    type="text"
                    required
                    disabled={isVerified}
                    placeholder="e.g. 192.168.244.97"
                    value={lanforgeIp}
                    onChange={(e) => setLanforgeIp(e.target.value)}
                    className={`w-full px-4 py-2.5 bg-white/5 border rounded-lg text-white placeholder-white/30 text-sm outline-none transition-all font-mono ${
                      isVerified 
                        ? "border-emerald-500/30 bg-emerald-500/5 text-emerald-300" 
                        : "border-white/10 focus:border-cyan-500/40 focus:bg-white/[0.08]"
                    }`}
                  />
                </div>
                {connectError && (
                  <div className="text-rose-400 bg-rose-500/10 border border-rose-500/20 text-xs p-3 rounded-lg flex gap-2 text-left">
                    <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                    <span>{connectError}</span>
                  </div>
                )}
                {!isVerified ? (
                  <button
                    onClick={handleConnect}
                    disabled={isConnecting}
                    className="w-full py-3 bg-white text-black font-semibold text-xs uppercase tracking-wider rounded-lg hover:bg-white/90 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
                  >
                    {isConnecting ? (
                      <>
                        <span className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin" />
                        Verifying IP...
                      </>
                    ) : (
                      "Verify LANForge IP"
                    )}
                  </button>
                ) : (
                  <button
                    onClick={() => setIsConnected(true)}
                    className="w-full py-3 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold text-xs uppercase tracking-wider rounded-lg hover:from-cyan-400 hover:to-blue-500 transition-all flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-cyan-500/10"
                  >
                    Launch AI Console
                  </button>
                )}
              </motion.div>
            </div>
          </div>
          
          {/* Email Request Modal */}
          <AnimatePresence>
            {showEmailForm && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="absolute inset-0 bg-black/60 backdrop-blur-sm z-30 flex items-center justify-center p-6"
              >
                <motion.div
                  initial={{ scale: 0.95, y: 10 }}
                  animate={{ scale: 1, y: 0 }}
                  exit={{ scale: 0.95, y: 10 }}
                  className="w-full max-w-md p-6 bg-black/85 border border-white/10 rounded-2xl shadow-2xl relative"
                >
                  <button
                    onClick={() => setShowEmailForm(false)}
                    className="absolute top-4 right-4 p-1.5 rounded-full hover:bg-white/10 text-white/60 hover:text-white transition-colors cursor-pointer"
                  >
                    <X className="w-4 h-4" />
                  </button>
                  
                  <h3 className="text-base font-semibold mb-1 text-white">Request Enterprise Access</h3>
                  <p className="text-xs text-white/50 mb-4 leading-relaxed">
                    Provide your corporate email to receive immediate validation demos and early network automation updates.
                  </p>

                  <form onSubmit={handleEmailSubmit} className="flex flex-col gap-3">
                    <input
                      type="email"
                      required
                      placeholder="Enter your enterprise email..."
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-lg text-white placeholder-white/30 text-sm outline-none focus:border-white/30"
                    />
                    
                    <button
                      type="submit"
                      disabled={emailSubmitted}
                      className="w-full py-2.5 bg-white text-black font-semibold text-xs uppercase tracking-wider rounded-lg hover:bg-white/90 transition-colors flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
                    >
                      {emailSubmitted ? (
                        <>
                          <Check className="w-4 h-4 text-black" />
                          Submitted Successfully
                        </>
                      ) : (
                        "Submit Request"
                      )}
                    </button>
                  </form>
                </motion.div>
              </motion.div>
            )}
          </AnimatePresence>
        </>
      ) : (
        // ==========================================
        // 2. STUNNING FULLSCREEN DASHBOARD (CONNECTED WORKSPACE)
        // ==========================================
        <div className="flex-1 flex flex-col p-6 overflow-hidden bg-black/95">
          {/* Dashboard Header */}
          <div className="flex items-center justify-between border-b border-white/10 pb-4 mb-4 select-none shrink-0">
            <div className="flex items-center gap-3">
              <Network className="w-5 h-5 text-white" />
              <span className="font-semibold text-base tracking-tight font-sans">LANForge AI Console Workspace</span>
              <span className="flex items-center gap-1.5 px-3 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 text-xs border border-emerald-500/20 font-mono">
                <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-ping" />
                Connected to {lanforgeIp}
              </span>
              
              {/* Dynamic inventory counts in header */}
              <div className="hidden md:flex gap-4 text-[10px] text-white/50 bg-white/5 border border-white/10 px-3 py-1 rounded-full ml-3 font-mono">
                <span>Stations: <strong className="text-emerald-400">{inventory?.stations?.length || 0}</strong></span>
                <span>Radios: <strong className="text-cyan-400">{inventory?.radios?.length || 0}</strong></span>
                <span>Ethernet: <strong className="text-blue-400">{inventory?.ethernet?.length || 0}</strong></span>
                <span>Resources: <strong className="text-white">{(inventory?.stations?.length || 0) + (inventory?.radios?.length || 0) + (inventory?.ethernet?.length || 0)}</strong></span>
              </div>
            </div>
            
            <button
              onClick={() => {
                setIsConnected(false);
                setIsVerified(false);
                setInventory({ stations: [], ethernet: [], radios: [] });
                setQueryResult(null);
                setExecutionResult(null);
                setTerminalLines([]);
              }}
              className="px-4 py-1.5 rounded-lg bg-rose-500/10 text-rose-400 hover:bg-rose-500/20 transition-all cursor-pointer border border-rose-500/20 text-xs font-semibold uppercase tracking-wider"
            >
              Logout
            </button>
          </div>

          {/* Connected Workspace Split-Panel Content */}
          <div className="flex-1 flex gap-6 overflow-hidden min-h-0">
            {/* Left Side: ChatGPT Chat Interface */}
            <div className="flex-1 flex flex-col min-h-0 bg-white/[0.02] border border-white/5 rounded-xl overflow-hidden relative">
              {/* Chat Header */}
              <div className="flex items-center justify-between border-b border-white/10 px-4 py-3 bg-white/[0.01] select-none">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  <span className="text-xs font-semibold text-white/60 uppercase tracking-wider font-mono">LANForge Conversational Assistant</span>
                </div>
                {queryResult && (
                  <button
                    onClick={() => {
                      setQueryResult(null);
                      setChatState("idle");
                      setFormParams({});
                      setChatMessages([
                        { id: "1", sender: "ai", text: "Session reset. Ask for a new test or command." }
                      ]);
                    }}
                    className="text-[10px] text-white/40 hover:text-white uppercase tracking-wider font-bold cursor-pointer font-mono"
                  >
                    Clear Plan
                  </button>
                )}
              </div>

              {/* Chat messages viewport */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {chatMessages.map((msg, index) => (
                  <ChatMessage
                    key={msg.id}
                    msg={msg}
                    formParams={formParams}
                    setFormParams={setFormParams}
                    onAnswerSubmit={handleChatAnswerSubmit}
                    isActiveStep={
                      index === chatMessages.length - 1 &&
                      msg.controlType !== undefined
                    }
                  />
                ))}
                




                <div ref={messagesEndRef} />
              </div>

              {/* Chat Input Area */}
              <div className="border-t border-white/10 p-4 bg-white/[0.01] shrink-0">
                <form onSubmit={handleChatSubmit} className="flex gap-2 relative">
                  <input
                    type="text"
                    disabled={isQuerying || isExecuting || chatState !== "idle"}
                    placeholder={
                      chatState !== "idle" 
                        ? "Waiting for parameter inputs in chat cards above..." 
                        : "Ask to run a test, e.g. 'run dataplane test on station sta0000'..."
                    }
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    className="flex-1 bg-white/5 border border-white/10 rounded-lg px-4 py-2.5 text-sm text-white placeholder-white/30 outline-none focus:border-white/20 focus:bg-white/[0.07] disabled:opacity-50"
                  />
                  <button
                    type="submit"
                    disabled={isQuerying || isExecuting || chatState !== "idle"}
                    className="px-5 py-2.5 bg-white text-black hover:bg-white/90 disabled:opacity-50 transition-colors rounded-lg font-medium text-sm flex items-center justify-center cursor-pointer shrink-0"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                </form>
              </div>
            </div>

            {/* Right Side: Live Exec Logs Terminal Widget */}
            <div className="w-[45%] flex flex-col gap-4 overflow-hidden border-l border-white/10 pl-6 min-h-0">
              <div className="flex-1 flex flex-col bg-black border border-white/10 rounded-xl overflow-hidden font-mono text-sm shadow-2xl relative">
                {/* Terminal Header */}
                <div className="flex items-center justify-between bg-white/5 border-b border-white/10 px-4 py-2 text-xs text-white/60 select-none">
                  <div className="flex items-center gap-2">
                    <Terminal className="w-4 h-4" />
                    <span>SSH execution terminal</span>
                  </div>
                  <span className="text-white/40">PAGER=cat</span>
                </div>

                {/* Log Terminal Screen */}
                <div className="flex-1 p-4 overflow-y-auto text-emerald-400 space-y-2 select-text selection:bg-emerald-500 selection:text-black font-mono">
                  {terminalLines.length > 0 ? (
                    <div className="space-y-1.5 font-mono text-[11px] leading-relaxed">
                      {terminalLines.map((line, idx) => {
                        if (line.type === "system") {
                          return <div key={idx} className="text-white/50 italic">{line.text}</div>;
                        } else if (line.type === "command" || line.type === "command_actual") {
                          return (
                            <div key={idx} className="text-emerald-400 font-bold border-b border-white/5 pb-1 select-text">
                              {line.text}
                            </div>
                          );
                        } else if (line.type === "error") {
                          return <div key={idx} className="text-rose-400 font-bold bg-rose-500/10 p-2 rounded border border-rose-500/15">{line.text}</div>;
                        } else if (line.type === "stderr") {
                          return <pre key={idx} className="text-rose-400 bg-black whitespace-pre-wrap font-mono p-1">{line.text}</pre>;
                        } else if (line.type === "stdout") {
                          return <pre key={idx} className="text-emerald-300 bg-black whitespace-pre-wrap font-mono p-1">{line.text}</pre>;
                        } else {
                          return <div key={idx} className="text-cyan-400/90">{line.text}</div>;
                        }
                      })}
                    </div>
                  ) : (
                    <div className="text-white/30 h-full flex flex-col items-center justify-center text-center p-6 gap-2 font-sans">
                      <Terminal className="w-8 h-8 opacity-20" />
                      <p className="font-semibold text-sm">No active execution log.</p>
                      <p className="text-[11px] max-w-xs leading-normal">
                        Resolve a script, adjust parameters, and click "Run Automation" to stream console results here.
                      </p>
                    </div>
                  )}
                </div>
              </div>

              {/* Terminal footer status */}
              <div className="liquid-glass rounded-xl p-4 border border-white/5 flex items-center justify-between text-xs select-none">
                <span className="text-white/40">LANForge connection active</span>
                <span className="text-[10px] uppercase font-mono tracking-wider text-emerald-400 px-2 py-0.5 rounded-full bg-emerald-400/10 border border-emerald-400/25">Ready</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
