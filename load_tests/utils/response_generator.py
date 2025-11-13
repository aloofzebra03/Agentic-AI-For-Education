"""
Utility to generate realistic student responses based on current node state
"""
import random


class ResponseGenerator:
    
    # Responses for each pedagogical node
    APK_RESPONSES = [
        "I think a pendulum is something that swings back and forth",
        "I've seen pendulums in grandfather clocks",
        "Not really sure what affects how fast it swings",
        "Maybe the weight or length changes the time?",
        "I know it has something to do with gravity",
        "Is it like a swing at a playground?",
    ]
    
    CI_DEFINITION_ECHO = [
        "A pendulum is a weight suspended from a fixed point that swings back and forth",
        "It's a mass hanging from a string that oscillates",
        "A pendulum consists of a bob attached to a string or rod that swings",
        "The time period is the time taken for one complete oscillation",
        "Time period is how long it takes to swing back and forth once",
    ]
    
    GE_RESPONSES = [
        "So if I make the string longer, will it swing slower?",
        "What happens if I use a heavier weight?",
        "Does the angle I release it from matter?",
        "Can you show me an example?",
        "I'm confused about why length matters but weight doesn't",
        "So the time period depends on the length?",
    ]
    
    AR_CORRECT_RESPONSES = [
        "The length affects the time period",
        "Longer pendulums have longer time periods",
        "The weight doesn't affect the time period",
        "Only the length and gravity matter",
        "If you double the length, the time period increases",
    ]
    
    AR_INCORRECT_RESPONSES = [
        "I think heavier weights make it swing faster",
        "The angle must affect how long it takes",
        "Bigger swings take longer",
        "The material of the string matters",
    ]
    
    TC_RESPONSES = [
        "In a clock, the pendulum controls the timing",
        "Grandfather clocks use long pendulums for slower ticks",
        "Playground swings are like pendulums",
        "Metronomes for music use pendulums",
        "I've seen pendulums in science museums",
    ]
    
    RLC_QUIZ_RESPONSES = [
        "The time period depends on the length",
        "A longer pendulum has a longer time period",
        "Gravity affects the time period",
        "The mass doesn't change the time period",
    ]
    
    # Generic confused responses
    CONFUSED_RESPONSES = [
        "I'm not sure I understand",
        "Can you explain that again?",
        "This is confusing",
        "Wait, what?",
        "I don't get it",
    ]
    
    # Generic acknowledgment
    ACKNOWLEDGMENT = [
        "Okay",
        "I see",
        "Got it",
        "Makes sense",
        "Alright",
        "Yes",
    ]
    
    @classmethod
    def generate_response(cls, current_state: str, confused_probability: float = 0.1) -> str:

        # Sometimes students are confused regardless of node
        if random.random() < confused_probability:
            return random.choice(cls.CONFUSED_RESPONSES)
        
        if current_state == "START":
            return "Hi! I'm ready to learn."
        
        elif current_state == "APK":
            return random.choice(cls.APK_RESPONSES)
        
        elif current_state == "CI":
            return random.choice(cls.CI_DEFINITION_ECHO)
        
        elif current_state == "GE":
            return random.choice(cls.GE_RESPONSES)
        
        elif current_state == "AR":
            if random.random() < 0.8:
                return random.choice(cls.AR_CORRECT_RESPONSES)
            else:
                return random.choice(cls.AR_INCORRECT_RESPONSES)
        
        elif current_state == "TC":
            return random.choice(cls.TC_RESPONSES)
        
        elif current_state == "RLC":
            return random.choice(cls.RLC_QUIZ_RESPONSES)
        
        elif current_state.startswith("SIM_"):
            # Simulation responses
            return random.choice([
                "Let me try this simulation",
                "I'll observe what happens",
                "Interesting, I see the pattern",
                "This helps me understand",
            ])
        
        else:
            # Default acknowledgment
            return random.choice(cls.ACKNOWLEDGMENT)
    
    @classmethod
    def generate_persona_response(cls, persona_name: str, current_state: str) -> str:
        if "confused" in persona_name.lower():
            # Confused students ask more questions
            return cls.generate_response(current_state, confused_probability=0.4)
        
        elif "eager" in persona_name.lower():
            # Eager students give detailed responses
            if current_state == "APK":
                return "I know pendulums swing back and forth! I've learned about oscillations and I'm excited to understand the time period!"
            else:
                return cls.generate_response(current_state, confused_probability=0.0)
        
        elif "distracted" in persona_name.lower():
            # Distracted students give short, generic responses
            return random.choice(cls.ACKNOWLEDGMENT)
        
        elif "dull" in persona_name.lower():
            # Dull students need more prompting
            if random.random() < 0.3:
                return "I don't know"
            else:
                return cls.generate_response(current_state, confused_probability=0.2)
        
        else:
            # Default behavior
            return cls.generate_response(current_state)


# Quick test
if __name__ == "__main__":
    print("Testing ResponseGenerator...")
    print("=" * 80)
    
    nodes = ["START", "APK", "CI", "GE", "AR", "TC", "RLC"]
    
    for node in nodes:
        response = ResponseGenerator.generate_response(node)
        print(f"{node:10} → {response}")
    
    print("\n" + "=" * 80)
    print("Testing persona responses...")
    print("=" * 80)
    
    personas = ["Confused Student", "Eager Student", "Distracted Student"]
    
    for persona in personas:
        response = ResponseGenerator.generate_persona_response(persona, "APK")
        print(f"{persona:20} → {response}")
