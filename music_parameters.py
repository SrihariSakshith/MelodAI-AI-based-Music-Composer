import numpy as np
import pandas as pd

class MusicParameterProcessor:
    """
    Processes and enhances music parameters based on mood and energy level.
    Provides mappings from mood categories to music theory elements such as scales,
    chord progressions, rhythmic patterns, and keys.
    """

    def __init__(self):
        # Initialize mood-to-music theory mappings
        self.mood_theory_mappings = self.create_music_theory_mappings()
    
    def create_music_theory_mappings(self):
        """
        Returns a dictionary mapping mood categories to detailed music theory parameters.
        Each mood maps to possible scales, chord progressions, rhythmic patterns, and keys.
        """
        return {
            "happy": {
                "scales": ["major", "mixolydian", "lydian"],
                "chord_progressions": [["I", "V", "vi", "IV"], ["I", "vi", "IV", "V"]],
                "rhythmic_patterns": ["straight", "swing"],
                "typical_keys": ["C", "G", "D", "A", "E"]
            },
            "sad": {
                "scales": ["natural_minor", "harmonic_minor", "dorian"],
                "chord_progressions": [["i", "VII", "VI", "VII"], ["i", "iv", "V", "i"]],
                "rhythmic_patterns": ["straight", "rubato"],
                "typical_keys": ["Am", "Em", "Bm", "F#m"]
            },
            "calm": {
                "scales": ["major", "pentatonic", "aeolian"],
                "chord_progressions": [["I", "vi", "IV", "V"], ["I", "V", "vi", "iii"]],
                "rhythmic_patterns": ["legato", "sustained"],
                "typical_keys": ["C", "F", "Bb", "Eb"]
            },
            "energetic": {
                "scales": ["major", "minor", "blues"],
                "chord_progressions": [["I", "IV", "V", "I"], ["i", "VII", "VI", "VII"]],
                "rhythmic_patterns": ["staccato", "syncopated"],
                "typical_keys": ["E", "A", "D", "G"]
            },
            "mysterious": {
                "scales": ["harmonic_minor", "phrygian", "locrian"],
                "chord_progressions": [["i", "II", "i", "VII"], ["i", "bII", "bVII", "i"]],
                "rhythmic_patterns": ["irregular", "sparse"],
                "typical_keys": ["Dm", "Gm", "Cm", "F#m"]
            },
            "romantic": {
                "scales": ["major", "dorian", "natural_minor"],
                "chord_progressions": [["I", "vi", "ii", "V"], ["i", "VI", "III", "VII"]],
                "rhythmic_patterns": ["waltz", "ballad"],
                "typical_keys": ["F", "Bb", "Eb", "Ab"]
            }
        }
    
    def enhance_parameters(self, base_params):
        """
        Enhances base music parameters with detailed music theory elements based on mood.
        Randomly selects a chord progression, scale, rhythmic pattern, and key from the mood mapping.
        Also maps energy level to dynamics and texture.
        
        Args:
            base_params (dict): Dictionary with at least 'mood_category' and 'energy_level' keys.
        
        Returns:
            dict: Enhanced parameters including chord progression, scale, rhythm, key, dynamics, and texture.
        """
        mood = base_params["mood_category"]
        # Get mapping for the mood, default to 'calm' if not found
        mapping = self.mood_theory_mappings.get(mood, self.mood_theory_mappings["calm"])
        
        enhanced = base_params.copy()
        # Randomly select indices/types for each parameter
        enhanced.update({
            "chord_progression": np.random.choice(len(mapping["chord_progressions"])),  # index, will be replaced below
            "scale_type": np.random.choice(mapping["scales"]),
            "rhythmic_pattern": np.random.choice(mapping["rhythmic_patterns"]),
            "suggested_key": np.random.choice(mapping["typical_keys"]),
            "dynamics": self.map_energy_to_dynamics(base_params["energy_level"]),
            "texture": self.map_energy_to_texture(base_params["energy_level"])
        })
        
        # Replace index with actual chord progression list
        enhanced["chord_progression"] = mapping["chord_progressions"][enhanced["chord_progression"]]
        
        return enhanced
    
    def map_energy_to_dynamics(self, energy):
        """
        Maps a numeric energy level to a musical dynamics marking.
        Args:
            energy (int or float): Energy level (expected range: 1-10)
        Returns:
            str: Dynamics marking ('pp', 'mp', 'mf', 'f')
        """
        if energy <= 3: 
            return "pp"  # pianissimo (very soft)
        elif energy <= 5: 
            return "mp"  # mezzo-piano (moderately soft)
        elif energy <= 7: 
            return "mf"  # mezzo-forte (moderately loud)
        else: 
            return "f"   # forte (loud)
    
    def map_energy_to_texture(self, energy):
        """
        Maps a numeric energy level to a musical texture.
        Args:
            energy (int or float): Energy level (expected range: 1-10)
        Returns:
            str: Texture type ('monophonic', 'homophonic', 'polyphonic')
        """
        if energy <= 4: 
            return "monophonic"   # single melodic line
        elif energy <= 7: 
            return "homophonic"   # melody with accompaniment
        else: 
            return "polyphonic"