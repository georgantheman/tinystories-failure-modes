#!/usr/bin/env python3
"""
Categorize behavioral failure modes in TinyStories LLM outputs.
"""

import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Diagnose behavioral failure modes in TinyStories LLM outputs."
    )

    parser.add_argument(
        "--prompt_file",
        type=str,
        required=True,
        help="Path to JSONL file containing evaluation prompts.",
    )

    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to save failure categorization results (JSON).",
    )
    parser.add_argument("--model_path", type=str, required=True, help="Path to the model checkpoint (.pth)")

    return parser.parse_args()

import json

def load_prompts(path):
    prompts = []
    with open(path, 'r') as f:
        for line in f:
            prompts.append(json.loads(line))
    return prompts


import subprocess
import json

def generate_responses(model_path, prompts, tokenizer_path):
    responses = []
    for p_obj in prompts:
    # p_obj['prompt'] is the string: "<user> ... <assistant>"
        prompt_text = p_obj['prompt']

        cmd = [
            "poetry", "run", "python", "src/chat_with_tinystories_model.py",
            "--model_path", model_path,
            "--tokenizer_path", tokenizer_path,
            "--max_seq_len", "128", # Crucial: Must match your model architecture
            "--device", "mps",  # Use "cpu" if you aren't on a Mac
            "--prompt", prompt_text 
        ]

        print(f"Testing Category [{p_obj['category']}]: {prompt_text[7:50]}...")

        # Run the command and capture the output
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            full_output = result.stdout.strip()

            if "Generated: " in full_output:
                generated_part = full_output.split("Generated: ")[-1].strip()
            else:
                generated_part = "ERROR: Could not find Generated marker"
            
            
            responses.append({
                "prompt_info": p_obj,
                "generated_text": generated_part
            })
        else:
            print(f"Terminal Error for prompt: {result.stderr}")

    return responses

import os
def categorize_failures(responses):
    results = []
    # These match the categories in your chat_prompts.jsonl
    summary = {cat: {"pass": 0, "total": 0} for cat in [
        "location", "object_tracking", "pronoun", "math", "common_sense"
    ]}

    for res in responses:
        info = res["prompt_info"]
        category = info["category"]
        assistant_answer = res["generated_text"].lower()
        
        # Multi-Target Logic: Check if any correct answer exists in the response
        targets = info["target"] if isinstance(info["target"], list) else [info["target"]]
        
        # Focus on the first 5 words. This prevents "lucky" guesses
        # where the model rambles and eventually says the right word.
        answer_window = " ".join(assistant_answer.split()[:5])
        
        success = any(t.lower() in answer_window for t in targets)
        
        # Update summary counters
        if category in summary:
            summary[category]["total"] += 1
            if success:
                summary[category]["pass"] += 1
            
        results.append({
            "category": category,
            "prompt": info["prompt"],
            "generated_answer": assistant_answer,
            "success": success
        })

    return results, summary


def print_report(summary):
    print("\n" + "="*30)
    print("BASELINE FAILURE REPORT")
    print("="*30)
    print(f"{'Category':<18} | {'Accuracy':<10}")
    print("-" * 30)
    for cat, stats in summary.items():
        acc = (stats["pass"] / stats["total"] * 100) if stats["total"] > 0 else 0
        print(f"{cat:<18} | {acc:>8.1f}%")
    print("="*30)

import csv
from datetime import datetime

def save_results(results, summary, output_dir="eval_results"):
    # 1. Create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 2. Save Detailed JSON (Good for debugging why it failed)
    json_path = os.path.join(output_dir, f"detailed_results_{timestamp}.json")
    with open(json_path, 'w') as f:
        json.dump({"summary": summary, "results": results}, f, indent=4)
    
    # 3. Save Summary CSV (Perfect for your Final Report tables)
    csv_path = os.path.join(output_dir, f"summary_{timestamp}.csv")
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Pass", "Total", "Accuracy %"])
        for cat, stats in summary.items():
            acc = (stats["pass"] / stats["total"] * 100) if stats["total"] > 0 else 0
            writer.writerow([cat, stats["pass"], stats["total"], f"{acc:.2f}"])
            
    print(f"\nResults saved to:\n - {json_path}\n - {csv_path}")


def main():
    args = parse_args()
    
    # Use global paths or overwrite with args if you prefer
    MODEL_PATH = args.model_path
    TOKENIZER_PATH = "bpe_tokenizer_tinystories.pkl"
    PROMPT_PATH = args.prompt_file  # Use the CLI argument here!

    print(f"--- Starting Evaluation ---")
    print(f"Loading prompts from: {PROMPT_PATH}")
    
    prompts = load_prompts(PROMPT_PATH)
    responses = generate_responses(MODEL_PATH, prompts, TOKENIZER_PATH)
    
    results, summary = categorize_failures(responses)
    print_report(summary)
    
    # Save using your custom output directory from CLI args
    save_results(results, summary, output_dir=args.output)

if __name__ == "__main__":
    main()