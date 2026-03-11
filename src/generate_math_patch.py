import json
import random

def generate_math_patch(output_path, num_samples=2000):
    samples = []
    
    # Mapper for number-word consistency
    # We only need up to four, but kept five for safety in logic
    num_map = {
        0: "zero", 1: "one", 2: "two", 3: "three", 4: "four"
    }
    
    templates = [
        # Subtraction logic (keywords: away, left, loses, gave)
        ("I have {a} {obj}. I give {b} to you. How many are left?", "{res}"),
        ("There are {a} {obj} together. {b} go away. How many are left?", "{res}"),
        ("A {obj} has {a} legs. It loses {b}. How many legs now?", "{res}"),
        ("{a_cap} {obj} were swimming. {b_cap} swam away. How many are still swimming?", "{res}"),
        ("There are {a} {obj}. I eat {b}. How many are left?", "{res}"),
        
        # Addition logic (keywords: more, joined, total, together)
        ("I have {a} {obj}. You give me {b} more. How many total?", "{res}"),
        ("George has {a} {obj} and Sarah has {b} {obj}. How many do they have together?", "{res}"),
        ("The cat had {a} kittens. Then it had {b} more. How many kittens now?", "{res}"),
        ("{a_cap} {obj} were on the fence. {b_cap} more joined them. How many now?", "{res}"),
        ("I see {a} red {obj} and {b} green {obj}. How many {obj} total?", "{res}"),
        ("The boy found {a} {obj}. Then he found {b} more. How many total?", "{res}"),
        ("Mom bought {a} {obj}. Dad bought {b} more. How many {obj} in the house?", "{res}"),
        ("I have {a} {obj} in my hand and {b} in my pocket. How many total?", "{res}"),
        ("Look! {a} {obj} are flying. {b} more start to fly. How many now?", "{res}")
    ]
    
    objects = ["apples", "balls", "birds", "cats", "toy cars", "stars", "flowers", "cookies", 
               "fish", "shells", "bones", "eggs", "frogs", "planes", "kids", "socks"]

    for _ in range(num_samples):
        template_q, template_a = random.choice(templates)
        obj = random.choice(objects)
        
        # Determine Logic based on template keywords
        # Adjusted to ensure results stay within 0-4
        if any(word in template_q for word in ["away", "left", "loses", "give"]):
            a = random.randint(1, 4)
            b = random.randint(0, a) # Result will be 0 to 4
            result = a - b
        else:
            a = random.randint(1, 3)
            b = random.randint(1, 4-a) # Result will be 2 to 4
            result = a + b
        
        # FORCE WORDS: No digits allowed for this experiment
        val_a = num_map[a]
        val_b = num_map[b]
        val_res = num_map[result]

        # Formatting
        question = template_q.format(
            a=val_a, 
            b=val_b, 
            a_cap=val_a.capitalize(), 
            b_cap=val_b.capitalize(), 
            obj=obj
        )
        
        # Use simple, consistent answer formats
        answer_formats = [
            f"{val_res}",
            f"There are {val_res}.",
            f"Now I have {val_res}.",
            f"{val_res} {obj}."
        ]
        answer = random.choice(answer_formats)

        full_text = f"<user> {question} <assistant> {answer} <|endoftext|>"
        samples.append({"text": full_text})

    # Shuffle to ensure addition/subtraction are mixed
    random.shuffle(samples)

    with open(output_path, 'w') as f:
        for s in samples:
            f.write(json.dumps(s) + '\n')
            
    print(f"Generated {num_samples} word-only math samples (0-4) at {output_path}")

if __name__ == "__main__":
    generate_math_patch("data/math_patch.jsonl")