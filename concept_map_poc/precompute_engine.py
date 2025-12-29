"""
Pre-computation Engine - Character-Based Timing with gTTS
=========================================================
Generates all assets (audio, layout) using character-based timing.
This version uses ONLY gTTS and does NOT require MP3 duration reading.
"""

import os
import tempfile
import logging
import time
from typing import Dict, List, Tuple
import networkx as nx
from pathlib import Path
from gtts import gTTS

logger = logging.getLogger(__name__)


class PrecomputeEngine:
    """
    Pre-computes all visualization assets for smooth playback.
    Uses character-based timing with gTTS (no Edge-TTS, no MP3 duration reading).
    """
    
    def __init__(self, voice: str = "com", rate: str = "+0%", layout_style: str = "hierarchical"):
        """
        Initialize pre-computation engine with gTTS.
        
        Args:
            voice: gTTS TLD (default: "com" for Google.com voice)
                   Options: "com", "co.uk", "com.au", "co.in", etc.
            rate: Not used by gTTS (kept for API compatibility)
            layout_style: Graph layout algorithm (default: hierarchical)
                         Options: "hierarchical", "shell", "circular", "kamada-kawai", "spring"
        """
        self.voice = voice  # Actually TLD for gTTS
        self.rate = rate
        self.layout_style = layout_style
        self.temp_dir = tempfile.mkdtemp(prefix="concept_map_audio_")
        self.audio_files = []
        logger.info(f"🎤 Using gTTS with TLD: {voice}")
        logger.info(f"📐 Using layout: {layout_style}")
        logger.info(f"📁 Audio temp directory: {self.temp_dir}")
    
    def generate_audio_file(self, text: str, index: int, max_retries: int = 5) -> str:
        """
        Generate audio file using gTTS with retry logic for rate limiting.
        
        Args:
            text: Text to synthesize
            index: Index for filename
            max_retries: Maximum number of retry attempts (default: 5)
            
        Returns:
            Path to generated audio file, or None if all retries fail
        """
        output_file = os.path.join(self.temp_dir, f"audio_{index}.mp3")
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    # Exponential backoff with longer delays for rate limiting
                    # Wait: 3s, 6s, 12s, 24s, 48s
                    wait_time = 3 * (2 ** (attempt - 1))
                    logger.info(f"⏳ Rate limit detected. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}...")
                    time.sleep(wait_time)
                
                logger.info(f"🎤 Generating audio with gTTS (attempt {attempt + 1}/{max_retries}): \"{text[:50]}...\"")
                
                # Generate with gTTS
                tts = gTTS(text=text, lang='en', tld=self.voice, slow=False)
                tts.save(output_file)
                
                self.audio_files.append(output_file)
                logger.info(f"✅ Audio saved successfully: {output_file}")
                return output_file
                
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "Too Many Requests" in error_msg:
                    logger.warning(f"⚠️ Rate limited by gTTS (attempt {attempt + 1}/{max_retries}): {e}")
                else:
                    logger.warning(f"⚠️ gTTS attempt {attempt + 1}/{max_retries} failed: {e}")
                
                if attempt == max_retries - 1:
                    logger.error(f"❌ gTTS failed after {max_retries} attempts. Audio generation aborted.")
                    logger.error(f"   This may be due to rate limiting from Google's TTS service.")
                    logger.error(f"   Please try again in a few minutes.")
                    return None
        
        return None
    
    def generate_all_audio(self, timeline: Dict) -> Dict:
        """
        Pre-generate audio for the full timeline using gTTS.
        
        **CHARACTER-BASED TIMING APPROACH:**
        - Does NOT require MP3 duration reading
        - Does NOT rescale timings
        - Uses character-based timing from timeline_mapper.py
        - Timing is calculated as: char_count * 0.08 seconds (calibrated for gTTS)
        
        Args:
            timeline: Timeline dict from timeline_mapper
            
        Returns:
            Updated timeline with audio_file path (timings already accurate from character-based calculation)
        """
        logger.info("🎵 Pre-generating audio with CHARACTER-BASED timing (gTTS only)...")
        
        # Get full text from timeline
        full_text = timeline.get("full_text", "")
        
        if not full_text:
            logger.warning("⚠️ No full_text in timeline, falling back to sentences")
            # Fallback: use legacy sentence structure
            total_sentences = len(timeline["sentences"])
            for sentence_data in timeline["sentences"]:
                idx = sentence_data["index"]
                text = sentence_data["text"]
                
                logger.info(f"  🎤 Generating audio {idx + 1}/{total_sentences}: \"{text[:50]}...\"")
                
                audio_file = self.generate_audio_file(text, idx)
                sentence_data["audio_file"] = audio_file
            
            logger.info(f"✅ Generated {total_sentences} audio files (legacy mode)")
            return timeline
        
        # Generate audio file with gTTS
        logger.info(f"  🎤 Generating audio for full text: \"{full_text[:100]}...\"")
        audio_file = self.generate_audio_file(full_text, 0)
        
        if audio_file and os.path.exists(audio_file):
            # Store audio file in timeline (top-level for compatibility)
            timeline["audio_file"] = audio_file
            timeline["metadata"]["audio_file"] = audio_file
            
            # NO RESCALING - character-based timing is already accurate
            estimated_duration = timeline["metadata"].get("total_duration", 0.0)
            logger.info(f"✅ Audio generated successfully")
            logger.info(f"📊 Timeline duration (character-based): {estimated_duration:.2f}s")
            logger.info(f"ℹ️  Using character-based timing - NO rescaling needed")
        else:
            logger.error("❌ Audio generation failed")
        
        return timeline
    
    def calculate_positions(self, G: nx.DiGraph, concepts: List[Dict]) -> Dict[str, Tuple[float, float]]:
        """
        Calculate node positions using Smart Grid Layout.
        
        Smart Grid Layout Rules:
        - Root node at top center (0, 0)
        - 3 columns: x = -8, 0, +8
        - Sequential fill: left-to-right, top-to-bottom
        - Dynamic vertical spacing: -7, -14, -21, -28...
        
        Args:
            G: NetworkX directed graph
            concepts: List of concept dicts
            
        Returns:
            Dict mapping concept names to (x, y) positions
        """
        logger.info("📐 Calculating Smart Grid layout positions...")
        
        pos = {}
        
        # Find root node (no incoming edges)
        root_nodes = [n for n in G.nodes() if G.in_degree(n) == 0]
        
        if not root_nodes:
            logger.warning("⚠️ No root node found, using first node")
            root_nodes = [list(G.nodes())[0]] if G.nodes() else []
        
        # Smart Grid Layout
        COLUMNS = 3
        COL_X_POSITIONS = [-8.0, 0.0, 8.0]  # Fixed x positions
        VERTICAL_SPACING = 7.0  # Space between rows
        
        # Place root at top center
        if root_nodes:
            root = root_nodes[0]
            pos[root] = (0.0, 0.0)
            logger.info(f"  📍 Root '{root}' at (0, 0)")
        
        # Get non-root nodes sorted by importance
        non_root_nodes = [n for n in G.nodes() if n not in root_nodes]
        
        # Sort by importance (from concepts list)
        concept_dict = {c['name']: c for c in concepts}
        non_root_nodes_sorted = sorted(
            non_root_nodes,
            key=lambda n: concept_dict.get(n, {}).get('importance', 0),
            reverse=True
        )
        
        # Place nodes in grid (3 columns, sequential fill)
        for idx, node in enumerate(non_root_nodes_sorted):
            col = idx % COLUMNS
            row = idx // COLUMNS + 1  # +1 because root is at row 0
            
            x = COL_X_POSITIONS[col]
            y = -row * VERTICAL_SPACING
            
            pos[node] = (x, y)
            logger.debug(f"  📍 '{node}' at ({x}, {y})")
        
        logger.info(f"✅ Positioned {len(pos)} nodes in Smart Grid layout")
        return pos
    
    def _filter_edges_by_incoming_limit(
        self, 
        G: nx.DiGraph, 
        concepts: List[Dict],
        max_incoming: int = 2
    ) -> List[Tuple[str, str]]:
        """
        Filter edges to ensure each node has at most max_incoming edges.
        Root node has 0 incoming edges.
        
        Priority: Keep edges from more important nodes.
        
        Args:
            G: NetworkX directed graph
            concepts: List of concept dicts with importance scores
            max_incoming: Maximum incoming edges per node (except root)
            
        Returns:
            List of (source, target) tuples to keep
        """
        logger.info(f"🔗 Filtering edges: max {max_incoming} incoming per node...")
        
        # Create importance lookup
        concept_dict = {c['name']: c for c in concepts}
        
        # Find root nodes
        root_nodes = {n for n in G.nodes() if G.in_degree(n) == 0}
        
        edges_to_keep = []
        
        for node in G.nodes():
            if node in root_nodes:
                continue  # Root has no incoming edges
            
            # Get all incoming edges
            incoming = list(G.in_edges(node))
            
            if len(incoming) <= max_incoming:
                edges_to_keep.extend(incoming)
            else:
                # Sort by source importance (higher importance = keep)
                incoming_sorted = sorted(
                    incoming,
                    key=lambda e: concept_dict.get(e[0], {}).get('importance', 0),
                    reverse=True
                )
                
                # Keep top max_incoming edges
                edges_to_keep.extend(incoming_sorted[:max_incoming])
                
                dropped = len(incoming) - max_incoming
                logger.debug(f"  📉 Node '{node}': kept {max_incoming}/{len(incoming)} edges (dropped {dropped})")
        
        logger.info(f"✅ Filtered edges: {len(edges_to_keep)}/{G.number_of_edges()} kept")
        return edges_to_keep
    
    def prepare_graph(self, timeline: Dict) -> Tuple[nx.DiGraph, Dict]:
        """
        Prepare graph with positions and filtered edges.
        
        Args:
            timeline: Timeline dict with concepts and relationships
            
        Returns:
            (NetworkX graph, position dict)
        """
        logger.info("🌐 Preparing graph structure...")
        
        # Create directed graph
        G = nx.DiGraph()
        
        # Add nodes
        concepts = timeline.get("concepts", [])
        for concept in concepts:
            G.add_node(concept["name"])
        
        # Add all edges first
        relationships = timeline.get("relationships", [])
        for rel in relationships:
            if rel["from"] in G.nodes() and rel["to"] in G.nodes():
                G.add_edge(
                    rel["from"], 
                    rel["to"], 
                    label=rel.get("relationship", "")
                )
        
        logger.info(f"  �� Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges (before filtering)")
        
        # Filter edges (max 2 incoming per node)
        edges_to_keep = self._filter_edges_by_incoming_limit(G, concepts, max_incoming=2)
        
        # Create new filtered graph
        G_filtered = nx.DiGraph()
        G_filtered.add_nodes_from(G.nodes())
        
        for source, target in edges_to_keep:
            label = G[source][target].get("label", "")
            G_filtered.add_edge(source, target, label=label)
        
        logger.info(f"  📊 Filtered graph: {G_filtered.number_of_nodes()} nodes, {G_filtered.number_of_edges()} edges")
        
        # Calculate positions
        pos = self.calculate_positions(G_filtered, concepts)
        
        logger.info("✅ Graph preparation complete")
        return G_filtered, pos
    
    def cleanup(self):
        """Clean up temporary audio files."""
        import shutil
        if os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                logger.info(f"🧹 Cleaned up temp directory: {self.temp_dir}")
            except Exception as e:
                logger.warning(f"⚠️ Could not clean up temp directory: {e}")
    
    def precompute_all(self, timeline: Dict) -> Dict:
        """
        Main pre-computation method: Generate all assets.
        
        Args:
            timeline: Timeline from timeline_mapper
            
        Returns:
            Enhanced timeline with:
            - audio_file paths
            - pre_calculated_layout (node positions)
        """
        logger.info("=" * 70)
        logger.info("⚡ PRE-COMPUTATION PHASE (Character-Based Timing)")
        logger.info("=" * 70)
        
        # Step 1: Generate audio with gTTS (character-based timing already set)
        timeline = self.generate_all_audio(timeline)
        
        # Step 2: Prepare graph and calculate layout
        G, pos = self.prepare_graph(timeline)
        timeline["pre_calculated_layout"] = pos
        # Note: Don't store G in timeline (not JSON serializable)
        
        logger.info("=" * 70)
        logger.info("✅ PRE-COMPUTATION COMPLETE")
        logger.info("=" * 70)
        logger.info(f"  📊 Total concepts: {len(timeline.get('concepts', []))}")
        logger.info(f"  🎵 Audio file generated: {timeline.get('metadata', {}).get('audio_file', 'N/A')}")
        logger.info(f"  📐 Layout positions: {len(pos)}")
        logger.info(f"  🔗 Graph edges: {G.number_of_edges()}")
        logger.info("=" * 70)
        
        return timeline
