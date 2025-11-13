"""
Custom metrics collection for load testing
"""
import time
from typing import Dict, Any, List
from datetime import datetime


class MetricsCollector:
    
    def __init__(self):
        self.node_latencies: List[Dict[str, Any]] = []
        self.checkpoint_operations: List[Dict[str, Any]] = []
        self.llm_calls: List[Dict[str, Any]] = []
        self.state_transitions: List[Dict[str, Any]] = []
        self.graph_transitions: List[Dict[str, Any]] = []
        self.simulation_triggers: List[Dict[str, Any]] = []
        self.image_loads: List[Dict[str, Any]] = []
        self.video_loads: List[Dict[str, Any]] = []
        self.misconceptions: List[Dict[str, Any]] = []
        self.quiz_scores: List[float] = []
        self.session_completions: List[Dict[str, Any]] = []
        
    def record_node_transition(self, from_node: str, to_node: str, latency_ms: float):
        self.state_transitions.append({
            "timestamp": datetime.now().isoformat(),
            "from_node": from_node,
            "to_node": to_node,
            "latency_ms": latency_ms   
        })
    
    def record_checkpoint_operation(self, operation: str, thread_id: str, latency_ms: float):
        self.checkpoint_operations.append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation,  # "save" or "load"
            "thread_id": thread_id,
            "latency_ms": latency_ms
        })
    
    def record_llm_call(self, node: str, latency_ms: float, tokens: int = None):
        self.llm_calls.append({
            "timestamp": datetime.now().isoformat(),
            "node": node,
            "latency_ms": latency_ms,
            "tokens": tokens
        })
    
    def record_graph_transition(self, from_node: str, to_node: str, message_index: int):
        self.graph_transitions.append({
            "timestamp": datetime.now().isoformat(),
            "from_node": from_node,
            "to_node": to_node,
            "message_index": message_index
        })
    
    def record_simulation_trigger(self, node: str):
        self.simulation_triggers.append({
            "timestamp": datetime.now().isoformat(),
            "node": node
        })
    
    def record_image_load(self, node: str, image_node: str):
        self.image_loads.append({
            "timestamp": datetime.now().isoformat(),
            "node": node,
            "image_node": image_node
        })
    
    def record_video_load(self, node: str, video_node: str):
        self.video_loads.append({
            "timestamp": datetime.now().isoformat(),
            "node": node,
            "video_node": video_node
        })
    
    def record_misconception(self, node: str):
        self.misconceptions.append({
            "timestamp": datetime.now().isoformat(),
            "node": node
        })
    
    def record_quiz_score(self, score: float):
        self.quiz_scores.append(score)
    
    def record_session_completion(self, thread_id: str, turn_count: int):
        self.session_completions.append({
            "timestamp": datetime.now().isoformat(),
            "thread_id": thread_id,
            "turn_count": turn_count
        })
    
    def get_node_latency_stats(self) -> Dict[str, Dict[str, float]]:
        stats = {}
        
        for transition in self.state_transitions:
            node = transition["to_node"]
            latency = transition["latency_ms"]
            
            if node not in stats:
                stats[node] = {
                    "count": 0,
                    "total": 0,
                    "min": float('inf'),
                    "max": 0
                }
            
            stats[node]["count"] += 1
            stats[node]["total"] += latency
            stats[node]["min"] = min(stats[node]["min"], latency)
            stats[node]["max"] = max(stats[node]["max"], latency)
        
        # Calculate averages
        for node in stats:
            stats[node]["avg"] = stats[node]["total"] / stats[node]["count"]
        
        return stats
    
    def get_checkpoint_stats(self) -> Dict[str, Any]:
        if not self.checkpoint_operations:
            return {}
        
        save_ops = [op for op in self.checkpoint_operations if op["operation"] == "save"]
        load_ops = [op for op in self.checkpoint_operations if op["operation"] == "load"]
        
        stats = {
            "total_operations": len(self.checkpoint_operations),
            "save_count": len(save_ops),
            "load_count": len(load_ops)
        }
        
        if save_ops:
            save_latencies = [op["latency_ms"] for op in save_ops]
            stats["save_avg_ms"] = sum(save_latencies) / len(save_latencies)
            stats["save_max_ms"] = max(save_latencies)
        
        if load_ops:
            load_latencies = [op["latency_ms"] for op in load_ops]
            stats["load_avg_ms"] = sum(load_latencies) / len(load_latencies)
            stats["load_max_ms"] = max(load_latencies)
        
        return stats
    
    def get_summary(self) -> Dict[str, Any]:
        return {
            "node_latencies": self.get_node_latency_stats(),
            "checkpoint_stats": self.get_checkpoint_stats(),
            "total_transitions": len(self.state_transitions),
            "total_checkpoint_ops": len(self.checkpoint_operations),
            "total_llm_calls": len(self.llm_calls),
            "total_simulations": len(self.simulation_triggers),
            "total_images": len(self.image_loads),
            "total_videos": len(self.video_loads),
            "total_misconceptions": len(self.misconceptions),
            "avg_quiz_score": sum(self.quiz_scores) / len(self.quiz_scores) if self.quiz_scores else 0,
            "completed_sessions": len(self.session_completions)
        }
    
    def print_summary(self):
        print("\n" + "=" * 80)
        print("📊 CUSTOM METRICS SUMMARY")
        print("=" * 80)
        
        # Node latencies
        node_stats = self.get_node_latency_stats()
        if node_stats:
            print("\n🔄 Node Transition Latencies:")
            print(f"{'Node':<15} {'Count':<10} {'Avg (ms)':<12} {'Min (ms)':<12} {'Max (ms)':<12}")
            print("-" * 80)
            for node, stats in sorted(node_stats.items()):
                print(f"{node:<15} {stats['count']:<10} {stats['avg']:<12.2f} {stats['min']:<12.2f} {stats['max']:<12.2f}")
        
        # Checkpoint stats
        checkpoint_stats = self.get_checkpoint_stats()
        if checkpoint_stats:
            print("\n💾 Checkpoint Operations:")
            print(f"Total Operations: {checkpoint_stats.get('total_operations', 0)}")
            if "save_avg_ms" in checkpoint_stats:
                print(f"Save - Count: {checkpoint_stats['save_count']}, Avg: {checkpoint_stats['save_avg_ms']:.2f}ms, Max: {checkpoint_stats['save_max_ms']:.2f}ms")
            if "load_avg_ms" in checkpoint_stats:
                print(f"Load - Count: {checkpoint_stats['load_count']}, Avg: {checkpoint_stats['load_avg_ms']:.2f}ms, Max: {checkpoint_stats['load_max_ms']:.2f}ms")
        
        # Additional metrics
        print(f"\n🎯 LangGraph-Specific Metrics:")
        print(f"Total Graph Transitions: {len(self.graph_transitions)}")
        print(f"Simulations Triggered: {len(self.simulation_triggers)}")
        print(f"Images Loaded: {len(self.image_loads)}")
        print(f"Videos Loaded: {len(self.video_loads)}")
        print(f"Misconceptions Detected: {len(self.misconceptions)}")
        
        if self.quiz_scores:
            avg_score = sum(self.quiz_scores) / len(self.quiz_scores)
            print(f"Quiz Scores - Count: {len(self.quiz_scores)}, Avg: {avg_score:.2f}")
        
        if self.session_completions:
            avg_turns = sum(s["turn_count"] for s in self.session_completions) / len(self.session_completions)
            print(f"Completed Sessions: {len(self.session_completions)}, Avg Turns: {avg_turns:.1f}")
        
        print("\n" + "=" * 80)


# Global metrics collector instance
global_metrics = MetricsCollector()
