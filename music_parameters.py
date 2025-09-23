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
            return "polyphonic"   # multiple independent melodic lines
    
    def get_tempo_range(self, mood, energy):
        """
        Get appropriate tempo range based on mood and energy level.
        
        Args:
            mood (str): Mood category
            energy (int): Energy level (1-10)
            
        Returns:
            tuple: (min_tempo, max_tempo) in BPM
        """
        base_ranges = {
            "happy": (120, 140),
            "sad": (60, 80),
            "calm": (70, 90),
            "energetic": (130, 160),
            "mysterious": (80, 100),
            "romantic": (90, 110),
            "epic": (110, 130),
            "anxious": (100, 120)
        }
        
        base_min, base_max = base_ranges.get(mood, (90, 120))
        
        # Adjust based on energy level
        energy_factor = (energy - 5) * 5  # -20 to +25 BPM adjustment
        adjusted_min = max(60, base_min + energy_factor)
        adjusted_max = min(180, base_max + energy_factor)
        
        return (int(adjusted_min), int(adjusted_max))
    
    def get_instrumentation_suggestions(self, mood, energy, texture):
        """
        Suggest instrumentation based on mood, energy, and texture.
        
        Args:
            mood (str): Mood category
            energy (int): Energy level (1-10)
            texture (str): Musical texture
            
        Returns:
            dict: Suggested instruments by category
        """
        instruments = {
            "happy": {
                "lead": ["acoustic guitar", "piano", "violin", "flute"],
                "harmony": ["piano", "strings", "acoustic guitar"],
                "rhythm": ["drums", "percussion", "bass guitar"],
                "color": ["brass section", "woodwinds", "bells"]
            },
            "sad": {
                "lead": ["piano", "cello", "violin", "acoustic guitar"],
                "harmony": ["strings", "piano", "pad synth"],
                "rhythm": ["soft drums", "bass", "minimal percussion"],
                "color": ["solo violin", "oboe", "french horn"]
            },
            "calm": {
                "lead": ["piano", "acoustic guitar", "flute", "harp"],
                "harmony": ["strings", "pad synth", "piano"],
                "rhythm": ["light percussion", "soft bass"],
                "color": ["ambient pads", "nature sounds", "chimes"]
            },
            "energetic": {
                "lead": ["electric guitar", "synthesizer", "brass", "violin"],
                "harmony": ["power chords", "synth pads", "strings"],
                "rhythm": ["full drum kit", "bass guitar", "percussion"],
                "color": ["electric guitar solos", "brass stabs", "synth leads"]
            },
            "mysterious": {
                "lead": ["theremin", "solo violin", "piano", "synthesizer"],
                "harmony": ["dark pads", "strings", "minor chords"],
                "rhythm": ["minimal drums", "deep bass", "irregular percussion"],
                "color": ["ambient textures", "sound effects", "dissonant harmonies"]
            },
            "romantic": {
                "lead": ["piano", "violin", "cello", "acoustic guitar"],
                "harmony": ["strings", "piano", "harp"],
                "rhythm": ["soft drums", "bass", "light percussion"],
                "color": ["solo instruments", "lush strings", "gentle brass"]
            }
        }
        
        mood_instruments = instruments.get(mood, instruments["calm"])
        
        # Adjust based on energy and texture
        if energy <= 3:
            # Low energy - minimal instrumentation
            return {
                "primary": mood_instruments["lead"][:2],
                "secondary": mood_instruments["harmony"][:1],
                "rhythm": mood_instruments["rhythm"][:1] if texture != "monophonic" else []
            }
        elif energy >= 8:
            # High energy - full instrumentation
            return {
                "primary": mood_instruments["lead"],
                "secondary": mood_instruments["harmony"] + mood_instruments["color"][:2],
                "rhythm": mood_instruments["rhythm"]
            }
        else:
            # Medium energy - balanced instrumentation
            return {
                "primary": mood_instruments["lead"][:3],
                "secondary": mood_instruments["harmony"][:2],
                "rhythm": mood_instruments["rhythm"][:2]
            }
    
    def get_genre_suggestions(self, mood, energy):
        """
        Suggest musical genres based on mood and energy.
        
        Args:
            mood (str): Mood category
            energy (int): Energy level (1-10)
            
        Returns:
            list: Suggested genres
        """
        genre_map = {
            ("happy", "low"): ["folk", "acoustic", "indie pop", "bossa nova"],
            ("happy", "medium"): ["pop", "indie rock", "jazz", "swing"],
            ("happy", "high"): ["dance", "electronic", "rock", "funk"],
            
            ("sad", "low"): ["ambient", "neo-classical", "folk ballad", "blues"],
            ("sad", "medium"): ["indie folk", "alternative rock", "jazz ballad"],
            ("sad", "high"): ["grunge", "emo", "post-rock"],
            
            ("calm", "low"): ["ambient", "new age", "classical", "meditation"],
            ("calm", "medium"): ["acoustic", "folk", "soft jazz", "chillout"],
            ("calm", "high"): ["indie rock", "soft electronic", "world music"],
            
            ("energetic", "low"): ["upbeat folk", "light rock", "pop"],
            ("energetic", "medium"): ["rock", "electronic", "funk", "dance"],
            ("energetic", "high"): ["EDM", "metal", "punk", "hardcore"],
            
            ("mysterious", "low"): ["dark ambient", "experimental", "minimal"],
            ("mysterious", "medium"): ["cinematic", "post-rock", "electronic"],
            ("mysterious", "high"): ["industrial", "dark electronic", "progressive"],
            
            ("romantic", "low"): ["classical", "acoustic ballad", "jazz standard"],
            ("romantic", "medium"): ["pop ballad", "R&B", "soft rock"],
            ("romantic", "high"): ["passionate rock", "latin", "tango"]
        }
        
        energy_category = "low" if energy <= 3 else "high" if energy >= 7 else "medium"
        return genre_map.get((mood, energy_category), ["contemporary", "crossover"])
    
    def generate_advanced_parameters(self, base_params):
        """
        Generate comprehensive advanced parameters for music composition.
        
        Args:
            base_params (dict): Basic parameters from mood analysis
            
        Returns:
            dict: Comprehensive parameter set with advanced features
        """
        enhanced = self.enhance_parameters(base_params)
        mood = base_params["mood_category"]
        energy = base_params["energy_level"]
        
        # Add advanced parameters
        tempo_range = self.get_tempo_range(mood, energy)
        enhanced["tempo_range"] = tempo_range
        enhanced["suggested_tempo"] = np.random.randint(tempo_range[0], tempo_range[1] + 1)
        
        # Update tempo in base params if it exists
        if "tempo" in enhanced:
            enhanced["tempo"] = enhanced["suggested_tempo"]
        
        enhanced["instrumentation"] = self.get_instrumentation_suggestions(mood, energy, enhanced["texture"])
        enhanced["genre_suggestions"] = self.get_genre_suggestions(mood, energy)
        
        # Add time signature suggestions
        enhanced["time_signature"] = self.get_time_signature(mood, energy)
        
        # Add harmonic complexity
        enhanced["harmonic_complexity"] = self.get_harmonic_complexity(energy)
        
        # Add production style
        enhanced["production_style"] = self.get_production_style(mood, energy)
        
        return enhanced
    
    def get_time_signature(self, mood, energy):
        """Get appropriate time signature based on mood and energy."""
        if mood in ["romantic", "calm"]:
            return np.random.choice(["4/4", "3/4", "6/8"], p=[0.5, 0.3, 0.2])
        elif mood == "energetic" and energy >= 7:
            return np.random.choice(["4/4", "7/8", "5/4"], p=[0.7, 0.2, 0.1])
        elif mood == "mysterious":
            return np.random.choice(["4/4", "5/4", "7/8", "3/4"], p=[0.4, 0.3, 0.2, 0.1])
        else:
            return "4/4"
    
    def get_harmonic_complexity(self, energy):
        """Determine harmonic complexity based on energy level."""
        if energy <= 3:
            return "simple"  # Basic triads
        elif energy <= 6:
            return "moderate"  # 7th chords, some extensions
        else:
            return "complex"  # Extended chords, alterations, jazz harmony
    
    def get_production_style(self, mood, energy):
        """Suggest production style based on mood and energy."""
        styles = {
            ("happy", "low"): "acoustic, natural reverb, warm",
            ("happy", "medium"): "polished, moderate compression, bright",
            ("happy", "high"): "energetic, heavy compression, wide stereo",
            
            ("sad", "low"): "intimate, close-mic, minimal processing",
            ("sad", "medium"): "atmospheric, reverb, gentle compression",
            ("sad", "high"): "dramatic, dynamic range, emotional processing",
            
            ("calm", "low"): "spacious, natural reverb, soft",
            ("calm", "medium"): "balanced, subtle effects, clean",
            ("calm", "high"): "lush, rich harmonics, full sound",
            
            ("energetic", "low"): "punchy, tight, focused",
            ("energetic", "medium"): "driving, compressed, powerful",
            ("energetic", "high"): "aggressive, heavily processed, intense",
            
            ("mysterious", "low"): "dark, atmospheric, experimental",
            ("mysterious", "medium"): "cinematic, spatial effects, mysterious",
            ("mysterious", "high"): "intense, dramatic processing, complex",
            
            ("romantic", "low"): "intimate, warm, gentle",
            ("romantic", "medium"): "lush, romantic reverb, smooth",
            ("romantic", "high"): "passionate, dynamic, expressive"
        }
        
        energy_category = "low" if energy <= 3 else "high" if energy >= 7 else "medium"
        return styles.get((mood, energy_category), "balanced, natural, clean")