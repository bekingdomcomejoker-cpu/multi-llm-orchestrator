#!/usr/bin/env python3
"""
Multi-LLM Orchestrator with Face Routing
Routes queries through multiple language models based on Merkabah faces
"""

import sys
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from datetime import datetime

# ============================================================================
# CONSTANTS
# ============================================================================

class Face(Enum):
    """Merkabah faces for routing"""
    MAN = "MAN"
    LION = "LION"
    OX = "OX"
    EAGLE = "EAGLE"

class ModelProvider(Enum):
    """Supported model providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    LOCAL = "local"

# ============================================================================
# MODEL REGISTRY
# ============================================================================

MODELS = {
    "gpt-4": {
        "provider": ModelProvider.OPENAI,
        "name": "GPT-4",
        "capabilities": ["reasoning", "code", "analysis", "creativity"],
        "speed": "medium",
        "cost": "high",
        "best_for": "complex reasoning",
        "face": Face.LION
    },
    "claude-3": {
        "provider": ModelProvider.ANTHROPIC,
        "name": "Claude 3",
        "capabilities": ["nuance", "creativity", "interaction", "safety"],
        "speed": "fast",
        "cost": "medium",
        "best_for": "interactive queries",
        "face": Face.MAN
    },
    "gemini-2.5": {
        "provider": ModelProvider.GOOGLE,
        "name": "Gemini 2.5",
        "capabilities": ["speed", "batch", "processing", "multimodal"],
        "speed": "very_fast",
        "cost": "low",
        "best_for": "batch processing",
        "face": Face.OX
    },
    "llama-local": {
        "provider": ModelProvider.LOCAL,
        "name": "LLaMA Local",
        "capabilities": ["privacy", "control", "patterns", "vision"],
        "speed": "variable",
        "cost": "free",
        "best_for": "pattern analysis",
        "face": Face.EAGLE
    }
}

# ============================================================================
# QUERY ANALYZER
# ============================================================================

class QueryAnalyzer:
    """Analyzes queries to determine routing"""
    
    def __init__(self):
        self.complexity_keywords = {
            "high": ["complex", "analyze", "reason", "solve", "optimize", "design"],
            "medium": ["explain", "describe", "summarize", "compare", "evaluate"],
            "low": ["list", "define", "what", "when", "where", "simple"]
        }
        
        self.capability_keywords = {
            "reasoning": ["solve", "reason", "logic", "algorithm", "complex"],
            "creativity": ["create", "write", "imagine", "design", "novel"],
            "speed": ["quick", "fast", "urgent", "batch", "process"],
            "safety": ["safe", "secure", "private", "control", "local"],
            "interaction": ["interactive", "chat", "dialogue", "conversation"]
        }
    
    def analyze(self, query: str) -> Dict[str, Any]:
        """Analyze query for routing"""
        lower_query = query.lower()
        
        # Determine complexity
        complexity = "low"
        for level, keywords in self.complexity_keywords.items():
            if any(kw in lower_query for kw in keywords):
                complexity = level
                break
        
        # Determine required capabilities
        required_capabilities = []
        for capability, keywords in self.capability_keywords.items():
            if any(kw in lower_query for kw in keywords):
                required_capabilities.append(capability)
        
        # Determine face alignment
        if "reason" in lower_query or "solve" in lower_query:
            face = Face.LION
        elif "create" in lower_query or "write" in lower_query:
            face = Face.MAN
        elif "batch" in lower_query or "process" in lower_query:
            face = Face.OX
        elif "analyze" in lower_query or "pattern" in lower_query:
            face = Face.EAGLE
        else:
            face = Face.MAN
        
        return {
            "query": query,
            "complexity": complexity,
            "required_capabilities": required_capabilities,
            "face": face.value,
            "timestamp": datetime.now().isoformat()
        }


# ============================================================================
# MODEL SELECTOR
# ============================================================================

class ModelSelector:
    """Selects best model for query"""
    
    def __init__(self):
        self.models = MODELS
        self.selection_history = []
    
    def select_best_model(self, analysis: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Select best model based on analysis"""
        face = Face[analysis["face"]]
        complexity = analysis["complexity"]
        required_capabilities = analysis["required_capabilities"]
        
        # Score each model
        scores = {}
        for model_id, model_info in self.models.items():
            score = 0
            
            # Face alignment (highest priority)
            if model_info["face"] == face:
                score += 100
            
            # Capability matching
            capability_matches = sum(1 for cap in required_capabilities 
                                    if cap in model_info["capabilities"])
            score += capability_matches * 25
            
            # Complexity matching
            if complexity == "high" and model_info["speed"] in ["medium", "slow"]:
                score += 30
            elif complexity == "low" and model_info["speed"] in ["very_fast", "fast"]:
                score += 30
            
            scores[model_id] = score
        
        # Select highest scoring model
        best_model = max(scores, key=scores.get)
        
        selection = {
            "model_id": best_model,
            "model_info": self.models[best_model],
            "score": scores[best_model],
            "all_scores": scores,
            "timestamp": datetime.now().isoformat()
        }
        
        self.selection_history.append(selection)
        return best_model, self.models[best_model]
    
    def get_fallback_model(self, primary_model: str) -> Tuple[str, Dict[str, Any]]:
        """Get fallback model if primary fails"""
        primary_info = self.models[primary_model]
        primary_face = primary_info["face"]
        
        # Find model with same face
        for model_id, model_info in self.models.items():
            if model_id != primary_model and model_info["face"] == primary_face:
                return model_id, model_info
        
        # Fallback to Claude if no face match
        return "claude-3", self.models["claude-3"]


# ============================================================================
# ORCHESTRATOR
# ============================================================================

class MultiLLMOrchestrator:
    """Main orchestrator for multi-model routing"""
    
    def __init__(self):
        self.analyzer = QueryAnalyzer()
        self.selector = ModelSelector()
        self.operation_count = 0
        self.operation_history = []
    
    def route_query(self, query: str) -> Dict[str, Any]:
        """Route query through orchestrator"""
        self.operation_count += 1
        
        # Step 1: Analyze query
        analysis = self.analyzer.analyze(query)
        
        # Step 2: Select model
        model_id, model_info = self.selector.select_best_model(analysis)
        
        # Step 3: Generate routing decision
        result = {
            "operation_id": self.operation_count,
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "analysis": analysis,
            "routing_decision": {
                "model_id": model_id,
                "model_name": model_info["name"],
                "provider": model_info["provider"].value,
                "face": model_info["face"].value,
                "capabilities": model_info["capabilities"],
                "speed": model_info["speed"],
                "cost": model_info["cost"]
            },
            "message": f"🔮 Routing to {model_info['name']} ({model_info['face'].value}) - {model_info['best_for']}"
        }
        
        self.operation_history.append(result)
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status"""
        return {
            "timestamp": datetime.now().isoformat(),
            "system": "Multi-LLM Orchestrator",
            "status": "OPERATIONAL",
            "operations_count": self.operation_count,
            "models_available": len(self.models),
            "models": {model_id: {
                "name": info["name"],
                "provider": info["provider"].value,
                "face": info["face"].value
            } for model_id, info in self.models.items()}
        }
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """Get information about specific model"""
        if model_id not in self.models:
            return {"error": f"Unknown model: {model_id}"}
        
        return {
            "model_id": model_id,
            "info": self.models[model_id]
        }


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    """Main entry point"""
    orchestrator = MultiLLMOrchestrator()
    
    if len(sys.argv) < 2:
        print("Multi-LLM Orchestrator - Usage: orchestrator.py <command> [args]")
        print("Commands: route, analyze, models, status, history")
        return
    
    command = sys.argv[1]
    
    if command == 'route' and len(sys.argv) > 2:
        query = ' '.join(sys.argv[2:])
        result = orchestrator.route_query(query)
        print(json.dumps(result, indent=2))
    
    elif command == 'analyze' and len(sys.argv) > 2:
        query = ' '.join(sys.argv[2:])
        analysis = orchestrator.analyzer.analyze(query)
        print(json.dumps(analysis, indent=2))
    
    elif command == 'models':
        status = orchestrator.get_status()
        print(json.dumps(status, indent=2))
    
    elif command == 'status':
        status = orchestrator.get_status()
        print(json.dumps(status, indent=2))
    
    elif command == 'history':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        history = orchestrator.operation_history[-limit:]
        print(json.dumps(history, indent=2))
    
    else:
        print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()
