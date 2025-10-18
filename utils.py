# Utility functions and classes for Tic Tac Toe game

class PerformanceTracker:
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset performance metrics"""
        self.nodes_explored = 0
        self.pruned_nodes = 0
        self.total_decision_time = 0
    
    def increment_nodes_explored(self):
        """Increment the count of nodes explored"""
        self.nodes_explored += 1
    
    def increment_pruned_nodes(self):
        """Increment the count of pruned nodes (for Alpha-Beta)"""
        self.pruned_nodes += 1
    
    def update_performance(self, decision_time, nodes_explored):
        """Update performance metrics"""
        self.total_decision_time = decision_time
        # The nodes_explored is already tracked via increment_nodes_explored
    
    def get_metrics(self):
        """Get current performance metrics"""
        total_nodes = self.nodes_explored
        pruned_percentage = 0.0
        
        if total_nodes > 0:
            pruned_percentage = (self.pruned_nodes / total_nodes) * 100
            
        return {
            'decision_time': round(self.total_decision_time, 4),  # in milliseconds
            'nodes_explored': total_nodes,
            'pruned_nodes': self.pruned_nodes,
            'pruning_efficiency': round(pruned_percentage, 2)
        }
