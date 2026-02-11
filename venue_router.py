"""
Venue Router - Intelligent Query Routing to Optimal Subsystems
Routes queries to appropriate components based on type and context
Status: Production Ready v1.0.0
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import json

class QueryType(Enum):
    """Types of queries"""
    ANALYSIS = "analysis"
    EXPLORATION = "exploration"
    VERIFICATION = "verification"
    OPTIMIZATION = "optimization"
    TRAINING = "training"
    MONITORING = "monitoring"
    INTEGRATION = "integration"

class VenueType(Enum):
    """Types of venues (subsystems)"""
    AXIOM_ENGINE = "axiom-engine"
    FRAMING_ENGINE = "framing-engine"
    FLOW_MONITOR = "flow-monitor"
    INTENT_CLASSIFIER = "intent-classifier"
    TRUTH_DETECTOR = "contradiction-detector"
    MERKABAH_ROUTER = "merkabah-routing"
    LLM_ORCHESTRATOR = "multi-llm-orchestrator"
    DOMINIQUE_TRAINING = "dominique-training"
    MASTER_ORCHESTRATOR = "master-orchestrator"

@dataclass
class VenueProfile:
    """Profile of a venue (subsystem)"""
    venue_type: VenueType
    query_types: List[QueryType]
    effectiveness: float = 0.8
    latency_ms: float = 10.0
    reliability: float = 0.99
    enabled: bool = True

class VenueRouter:
    """
    Venue Router System
    Routes queries to optimal subsystems based on type and context
    """
    
    def __init__(self):
        self.initialized = False
        self.venues: Dict[VenueType, VenueProfile] = {}
        self.routing_history: List[Dict[str, Any]] = []
        self.effectiveness_scores: Dict[VenueType, float] = {}
        self.routing_rules: Dict[QueryType, List[VenueType]] = {}
        
    def initialize(self) -> bool:
        """Initialize venue router"""
        self._load_venue_profiles()
        self._load_routing_rules()
        self.initialized = True
        return True
    
    def _load_venue_profiles(self) -> None:
        """Load profiles for all venues"""
        profiles = [
            (VenueType.AXIOM_ENGINE, [QueryType.VERIFICATION, QueryType.ANALYSIS], 0.99, 5.0),
            (VenueType.FRAMING_ENGINE, [QueryType.ANALYSIS, QueryType.EXPLORATION], 0.95, 8.0),
            (VenueType.FLOW_MONITOR, [QueryType.MONITORING, QueryType.ANALYSIS], 0.98, 3.0),
            (VenueType.INTENT_CLASSIFIER, [QueryType.ANALYSIS, QueryType.INTEGRATION], 0.92, 10.0),
            (VenueType.TRUTH_DETECTOR, [QueryType.VERIFICATION, QueryType.ANALYSIS], 0.94, 12.0),
            (VenueType.MERKABAH_ROUTER, [QueryType.OPTIMIZATION, QueryType.INTEGRATION], 0.90, 15.0),
            (VenueType.LLM_ORCHESTRATOR, [QueryType.EXPLORATION, QueryType.TRAINING], 0.88, 20.0),
            (VenueType.DOMINIQUE_TRAINING, [QueryType.TRAINING, QueryType.OPTIMIZATION], 0.91, 25.0),
            (VenueType.MASTER_ORCHESTRATOR, [QueryType.INTEGRATION, QueryType.MONITORING], 0.96, 8.0),
        ]
        
        for venue_type, query_types, effectiveness, latency in profiles:
            self.venues[venue_type] = VenueProfile(
                venue_type=venue_type,
                query_types=query_types,
                effectiveness=effectiveness,
                latency_ms=latency,
                reliability=0.99
            )
            self.effectiveness_scores[venue_type] = effectiveness
    
    def _load_routing_rules(self) -> None:
        """Load routing rules for query types"""
        self.routing_rules = {
            QueryType.ANALYSIS: [
                VenueType.AXIOM_ENGINE,
                VenueType.FRAMING_ENGINE,
                VenueType.INTENT_CLASSIFIER,
            ],
            QueryType.EXPLORATION: [
                VenueType.FRAMING_ENGINE,
                VenueType.LLM_ORCHESTRATOR,
                VenueType.MERKABAH_ROUTER,
            ],
            QueryType.VERIFICATION: [
                VenueType.AXIOM_ENGINE,
                VenueType.TRUTH_DETECTOR,
                VenueType.FLOW_MONITOR,
            ],
            QueryType.OPTIMIZATION: [
                VenueType.MERKABAH_ROUTER,
                VenueType.DOMINIQUE_TRAINING,
                VenueType.MASTER_ORCHESTRATOR,
            ],
            QueryType.TRAINING: [
                VenueType.DOMINIQUE_TRAINING,
                VenueType.LLM_ORCHESTRATOR,
                VenueType.MASTER_ORCHESTRATOR,
            ],
            QueryType.MONITORING: [
                VenueType.FLOW_MONITOR,
                VenueType.MASTER_ORCHESTRATOR,
                VenueType.AXIOM_ENGINE,
            ],
            QueryType.INTEGRATION: [
                VenueType.MASTER_ORCHESTRATOR,
                VenueType.MERKABAH_ROUTER,
                VenueType.INTENT_CLASSIFIER,
            ],
        }
    
    def classify_query(self, query: str) -> QueryType:
        """Classify query type"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["analyze", "explain", "describe", "how"]):
            return QueryType.ANALYSIS
        elif any(word in query_lower for word in ["explore", "investigate", "discover", "what if"]):
            return QueryType.EXPLORATION
        elif any(word in query_lower for word in ["verify", "check", "validate", "confirm"]):
            return QueryType.VERIFICATION
        elif any(word in query_lower for word in ["optimize", "improve", "enhance", "better"]):
            return QueryType.OPTIMIZATION
        elif any(word in query_lower for word in ["train", "learn", "teach", "improve"]):
            return QueryType.TRAINING
        elif any(word in query_lower for word in ["monitor", "track", "watch", "status"]):
            return QueryType.MONITORING
        else:
            return QueryType.INTEGRATION
    
    def select_best_venue(self, query_type: QueryType) -> Optional[VenueType]:
        """Select best venue for query type"""
        candidates = self.routing_rules.get(query_type, [])
        
        if not candidates:
            return None
        
        # Score venues based on effectiveness and reliability
        best_venue = None
        best_score = -1.0
        
        for venue_type in candidates:
            if venue_type not in self.venues:
                continue
            
            venue = self.venues[venue_type]
            if not venue.enabled:
                continue
            
            # Score = effectiveness * reliability / latency
            score = (venue.effectiveness * venue.reliability) / (venue.latency_ms / 10.0)
            
            if score > best_score:
                best_score = score
                best_venue = venue_type
        
        return best_venue
    
    def route_query(self, query: str) -> Tuple[Optional[VenueType], Dict[str, Any]]:
        """Route query to optimal venue"""
        # Classify query
        query_type = self.classify_query(query)
        
        # Select best venue
        venue = self.select_best_venue(query_type)
        
        # Log routing
        routing_info = {
            "query": query,
            "query_type": query_type.value,
            "selected_venue": venue.value if venue else None,
            "candidates": [v.value for v in self.routing_rules.get(query_type, [])],
        }
        
        self.routing_history.append(routing_info)
        
        return venue, routing_info
    
    def get_venue_stats(self) -> Dict[str, Any]:
        """Get statistics for all venues"""
        stats = {}
        
        for venue_type, profile in self.venues.items():
            routed_count = sum(1 for r in self.routing_history if r["selected_venue"] == venue_type.value)
            stats[venue_type.value] = {
                "effectiveness": profile.effectiveness,
                "latency_ms": profile.latency_ms,
                "reliability": profile.reliability,
                "routed_queries": routed_count,
                "enabled": profile.enabled
            }
        
        return stats
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute venue router"""
        if not self.initialized:
            self.initialize()
        
        query = input_data.get("query", "")
        if not query:
            return {"status": "error", "message": "No query provided"}
        
        venue, routing_info = self.route_query(query)
        
        return {
            "status": "success",
            "component": "venue-router",
            "query": query,
            "query_type": routing_info["query_type"],
            "selected_venue": routing_info["selected_venue"],
            "candidates": routing_info["candidates"],
            "routing_stats": self.get_venue_stats()
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get router status"""
        return {
            "name": "venue-router",
            "version": "1.0.0",
            "status": "production",
            "initialized": self.initialized,
            "venues_available": len([v for v in self.venues.values() if v.enabled]),
            "total_venues": len(self.venues),
            "queries_routed": len(self.routing_history),
            "query_types": len(self.routing_rules)
        }

if __name__ == "__main__":
    router = VenueRouter()
    router.initialize()
    
    print(f"✅ Venue Router initialized")
    print(f"   Venues available: {len(router.venues)}")
    print(f"   Query types: {len(router.routing_rules)}")
    
    # Test routing
    test_queries = [
        "How do neural networks process information?",
        "What if we explored alternative architectures?",
        "Can you verify this claim?",
        "How can we optimize performance?",
        "Train the system on new data",
    ]
    
    for query in test_queries:
        venue, info = router.route_query(query)
        print(f"\n   Query: {query}")
        print(f"   Type: {info['query_type']}")
        print(f"   Routed to: {info['selected_venue']}")
    
    print(f"\n✅ Venue Router operational")
