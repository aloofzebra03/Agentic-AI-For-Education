"""
Custom metrics collection for load testing
"""
import time
from typing import Dict, Any, List
from datetime import datetime


class MetricsCollector:
    """Collect custom metrics beyond Locust's built-in metrics"""
    
    def __init__(self):
        self.node_latencies: List[Dict[str, Any]] = []
        self.checkpoint_operations: List[Dict[str, Any]] = []
        self.llm_calls: List[Dict[str, Any]] = []
        self.state_transitions: List[Dict[str, Any]] = []
        
    def record_node_transition(self, from_node: str, to_node: str, latency_ms: float):
        """Record a node transition with timing"""
        self.state_transitions.append({
            "timestamp": datetime.now().isoformat(),
            "from_node": from_node,
            "to_node": to_node,
            "latency_ms": latency_ms   
        })
    
    def record_checkpoint_operation(self, operation: str, thread_id: str, latency_ms: float):
        """Record checkpoint save/load operation"""
        self.checkpoint_operations.append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation,  # "save" or "load"
            "thread_id": thread_id,
            "latency_ms": latency_ms
        })
    
    def record_llm_call(self, node: str, latency_ms: float, tokens: int = None):
        """Record LLM API call"""
        self.llm_calls.append({
            "timestamp": datetime.now().isoformat(),
            "node": node,
            "latency_ms": latency_ms,
            "tokens": tokens
        })
    
    def get_node_latency_stats(self) -> Dict[str, Dict[str, float]]:
        """Calculate average, min, max latency per node"""
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
        """Get checkpoint operation statistics"""
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
        """Get overall summary of collected metrics"""
        return {
            "node_latencies": self.get_node_latency_stats(),
            "checkpoint_stats": self.get_checkpoint_stats(),
            "total_transitions": len(self.state_transitions),
            "total_checkpoint_ops": len(self.checkpoint_operations),
            "total_llm_calls": len(self.llm_calls)
        }
    
    def print_summary(self):
        """Print a formatted summary of metrics"""
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
        
        print("\n" + "=" * 80)


# Global metrics collector instance
global_metrics = MetricsCollector()
