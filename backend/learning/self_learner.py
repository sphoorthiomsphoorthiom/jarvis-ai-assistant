"""
Self-Learning AI Module
Implements continuous learning and improvement based on ai42z framework
"""

import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import numpy as np
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SelfLearner:
    """Self-learning system that improves from every interaction"""
    
    def __init__(self, knowledge_path: str = "data/knowledge_base.json"):
        self.knowledge_path = Path(knowledge_path)
        self.knowledge_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Learning parameters
        self.learning_interval = 7  # Extract insights every 7 steps
        self.step_counter = 0
        self.interactions_buffer = []
        
        # Knowledge storage
        self.knowledge_base = self._load_knowledge()
        self.best_practices = []
        self.learned_patterns = defaultdict(list)
        self.performance_metrics = {
            "total_interactions": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "avg_confidence": 0.0
        }
        
        logger.info("Self-learner initialized")
    
    def _load_knowledge(self) -> Dict:
        """Load existing knowledge base"""
        if self.knowledge_path.exists():
            with open(self.knowledge_path, 'r') as f:
                return json.load(f)
        return {
            "best_practices": [],
            "patterns": {},
            "improvements": []
        }
    
    def _save_knowledge(self):
        """Persist knowledge to disk"""
        with open(self.knowledge_path, 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)
        logger.info(f"Knowledge saved to {self.knowledge_path}")
    
    async def log_interaction(self, 
                            query: str, 
                            response: str, 
                            feedback: Optional[Dict] = None,
                            confidence: float = 0.0):
        """Log an interaction for learning"""
        interaction = {
            "query": query,
            "response": response,
            "feedback": feedback,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }
        
        self.interactions_buffer.append(interaction)
        self.step_counter += 1
        self.performance_metrics["total_interactions"] += 1
        
        # Update feedback metrics
        if feedback:
            rating = feedback.get("rating", 0)
            if rating >= 4:
                self.performance_metrics["positive_feedback"] += 1
            elif rating <= 2:
                self.performance_metrics["negative_feedback"] += 1
        
        # Trigger learning every N steps
        if self.step_counter >= self.learning_interval:
            await self._extract_insights()
            self.step_counter = 0
        
        logger.info(f"Interaction logged. Steps until learning: {self.learning_interval - self.step_counter}")
    
    async def _extract_insights(self):
        """Extract best practices and insights from recent interactions"""
        if not self.interactions_buffer:
            return
        
        logger.info(f"Extracting insights from {len(self.interactions_buffer)} interactions...")
        
        # Analyze successful interactions (high feedback ratings)
        successful = [i for i in self.interactions_buffer 
                     if i.get("feedback") and i["feedback"].get("rating", 0) >= 4]
        
        # Analyze failed interactions (low ratings)
        failed = [i for i in self.interactions_buffer 
                 if i.get("feedback") and i["feedback"].get("rating", 0) <= 2]
        
        # Extract patterns from successful interactions
        if successful:
            patterns = self._identify_patterns(successful)
            for pattern in patterns:
                if pattern not in self.best_practices:
                    self.best_practices.append(pattern)
                    self.knowledge_base["best_practices"].append({
                        "pattern": pattern,
                        "discovered": datetime.now().isoformat(),
                        "success_count": len([i for i in successful if pattern.lower() in i["query"].lower()])
                    })
        
        # Learn from failures
        if failed:
            improvements = self._identify_improvements(failed)
            for improvement in improvements:
                self.knowledge_base["improvements"].append({
                    "issue": improvement,
                    "identified": datetime.now().isoformat()
                })
        
        # Update average confidence
        confidences = [i["confidence"] for i in self.interactions_buffer]
        if confidences:
            self.performance_metrics["avg_confidence"] = np.mean(confidences)
        
        # Clear buffer and save
        self.interactions_buffer = []
        self._save_knowledge()
        
        logger.info(f"Insights extracted. Best practices: {len(self.best_practices)}")
    
    def _identify_patterns(self, interactions: List[Dict]) -> List[str]:
        """Identify common patterns in successful interactions"""
        patterns = []
        
        # Simple pattern detection based on query keywords
        query_words = defaultdict(int)
        for interaction in interactions:
            words = interaction["query"].lower().split()
            for word in words:
                if len(word) > 3:  # Ignore short words
                    query_words[word] += 1
        
        # Patterns are words that appear frequently
        threshold = len(interactions) * 0.3  # 30% of interactions
        for word, count in query_words.items():
            if count >= threshold:
                patterns.append(f"Queries about '{word}' tend to be successful")
        
        return patterns
    
    def _identify_improvements(self, interactions: List[Dict]) -> List[str]:
        """Identify areas for improvement from failed interactions"""
        improvements = []
        
        # Analyze feedback comments
        for interaction in interactions:
            feedback = interaction.get("feedback", {})
            comment = feedback.get("feedback", "")
            if comment:
                improvements.append(f"User feedback: {comment}")
        
        # Check for low confidence responses
        low_conf = [i for i in interactions if i["confidence"] < 0.5]
        if len(low_conf) / len(interactions) > 0.5:
            improvements.append("Many responses have low confidence - need better training data")
        
        return improvements
    
    def get_relevant_knowledge(self, query: str) -> Dict:
        """Retrieve relevant learned knowledge for a query"""
        relevant = {
            "best_practices": [],
            "similar_patterns": []
        }
        
        query_lower = query.lower()
        
        # Find relevant best practices
        for practice in self.knowledge_base.get("best_practices", []):
            pattern = practice["pattern"].lower()
            # Simple keyword matching
            if any(word in pattern for word in query_lower.split()):
                relevant["best_practices"].append(practice)
        
        return relevant
    
    def get_performance_summary(self) -> Dict:
        """Get learning performance summary"""
        total = self.performance_metrics["total_interactions"]
        positive = self.performance_metrics["positive_feedback"]
        negative = self.performance_metrics["negative_feedback"]
        
        success_rate = (positive / total * 100) if total > 0 else 0
        
        return {
            "total_interactions": total,
            "positive_feedback_count": positive,
            "negative_feedback_count": negative,
            "success_rate": round(success_rate, 2),
            "avg_confidence": round(self.performance_metrics["avg_confidence"], 2),
            "best_practices_learned": len(self.best_practices),
            "improvements_identified": len(self.knowledge_base.get("improvements", []))
        }
    
    async def continuous_improvement(self):
        """Continuously improve the model based on accumulated knowledge"""
        logger.info("Starting continuous improvement cycle...")
        
        # Analyze all accumulated knowledge
        summary = self.get_performance_summary()
        
        # If success rate is low, trigger model retraining/fine-tuning
        if summary["success_rate"] < 70 and summary["total_interactions"] > 100:
            logger.warning(f"Success rate is {summary['success_rate']}%. Consider model fine-tuning.")
            # Here you would trigger model retraining with accumulated data
        
        # Merge overlapping best practices
        self._consolidate_knowledge()
        
        logger.info("Continuous improvement cycle completed")
    
    def _consolidate_knowledge(self):
        """Consolidate and merge overlapping knowledge"""
        # Remove duplicate best practices
        seen = set()
        unique_practices = []
        
        for practice in self.knowledge_base.get("best_practices", []):
            pattern = practice["pattern"]
            if pattern not in seen:
                seen.add(pattern)
                unique_practices.append(practice)
        
        self.knowledge_base["best_practices"] = unique_practices
        self._save_knowledge()

# Singleton instance
_learner_instance = None

def get_self_learner() -> SelfLearner:
    """Get or create self-learner instance"""
    global _learner_instance
    if _learner_instance is None:
        _learner_instance = SelfLearner()
    return _learner_instance
