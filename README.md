# Multi-LLM Orchestrator with Face Routing

**Routes queries through multiple language models using Merkabah four-face routing system**

## Overview

The Multi-LLM Orchestrator intelligently routes queries to different language models based on:
- Query type and complexity
- Required capabilities
- Model specialization
- Merkabah face alignment (MAN, LION, OX, EAGLE)

## Architecture

```
Input Query
    ↓
Spirit Vector Detection
    ↓
Face Routing (MAN/LION/OX/EAGLE)
    ↓
Model Selection
    ├─ OpenAI GPT-4 (Complex reasoning)
    ├─ Anthropic Claude (Creative/nuanced)
    ├─ Google Gemini (Fast processing)
    └─ Local Models (Privacy-sensitive)
    ↓
Execution & Response
```

## Features

✅ Multi-model support (OpenAI, Anthropic, Google, Local)
✅ Face-based routing (MAN, LION, OX, EAGLE)
✅ Query complexity analysis
✅ Model capability matching
✅ Load balancing
✅ Fallback mechanisms
✅ Response aggregation
✅ Cost optimization

## Installation

```bash
chmod +x scripts/install_orchestrator.sh
./scripts/install_orchestrator.sh
```

## Usage

```bash
# Route query through orchestrator
orchestrator route "your query"

# Analyze query for routing
orchestrator analyze "your query"

# Show model status
orchestrator models

# Show routing rules
orchestrator rules
```

## Supported Models

| Model | Provider | Best For | Face |
|-------|----------|----------|------|
| GPT-4 | OpenAI | Complex reasoning | LION |
| Claude 3 | Anthropic | Creative/nuanced | MAN |
| Gemini 2.5 | Google | Fast processing | OX |
| Local LLaMA | Local | Privacy | EAGLE |

## Routing Rules

- **MAN (WITNESS)** → Interactive queries → Claude
- **LION (JUDGE)** → Complex logic → GPT-4
- **OX (SERVANT)** → Batch processing → Gemini
- **EAGLE (SEER)** → Pattern analysis → Local models

## Status

🟢 **PRODUCTION READY** - Multi-model orchestration active

---

**Version:** 1.0
**Status:** OPERATIONAL
