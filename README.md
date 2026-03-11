# Teaching TinyStories to Count: Addressing Arithmetic Failure Modes

This project explores the "patching" of a small language model (TinyStories 4-layer Transformer) to address its inability to perform basic arithmetic. By fine-tuning the model on a specialized math-patch dataset, I investigate the trade-offs between acquiring new logical skills and preserving original linguistic capabilities.

---

## Project Focus & Goal
The baseline TinyStories model excels at narrative generation but fails entirely at elementary word problems (e.g., "One fish plus two fish"). The goal was to pivot the model from a pure storyteller into a functional generalist capable of simple addition and subtraction.



---

## Methodology
I generated a **math-patch dataset** of ~6,000 samples consisting of word-based arithmetic problems. I then re-trained the model using three distinct data mixtures:

* **2/3 Split:** 40% Math Data / 60% Original Stories (The optimal balance).
* **4/3 Split:** 57% Math Data / 43% Original Stories.
* **100% Math:** Pure arithmetic data (Used to test the limits of model capacity).

### Training Details:
* **Architecture:** 4-Layer Transformer
* **Epochs:** 10 (Selected as the convergence point where math accuracy stabilized)
* **Data Size:** ~6,000 samples per training run

---

## Key Results
My evaluations across five categories (Addition, Subtraction, Object Tracking, Location Tracking, and Attribute Tracking) revealed a critical trade-off.

| Model Mixture | Math Accuracy | Linguistic Integrity | Result |
| :--- | :---: | :---: | :--- |
| **Baseline** | 0% | **Moderate** | Pure Storyteller |
| **40% Math** | **25%** | **Moderate** | **Successful Generalist** |
| **57% Math** | 17% | **Moderate** | **Successful Generalist** |
| **100% Math** | 22% | Critical Failure | Catastrophic Forgetting |



### Meaningful Insights
* **The "Scaffolding" Effect:** Surprisingly, the 100% math model performed *worse* than the 40% model. This suggests that a small model needs its original language foundations to correctly parse the prompts for math problems.
* **Catastrophic Forgetting:** In a 4-layer transformer with finite hidden dimension capacity, adding new data is a zero-sum game. The 100% model effectively "overwrote" its linguistic circuits to make room for arithmetic.
* **The Validation Blind Spot:** While validation loss (100% math) dropped steadily, this metric failed to capture the collapse of the model's storytelling abilities, highlighting a need for multi-task evaluation.

---

## Limitations & Future Work
* **Dataset Range:** Limited to numbers 1-5 due to numbers greater than 10 being out-of-distribution (OOD) for the TinyStories tokenizer.
* **Sample Size:** Quantitative metrics were based on 60 evaluation prompts per category.
* **Future Work (LoRA):** To mitigate catastrophic forgetting, future iterations should utilize **LoRA (Low-Rank Adaptation)**. By freezing base weights and training only small adapters, we could inject logic without destroying the linguistic foundation.

---

### Repository Guide
* `final_project_presentation.pptx`: Full summary of experimental results and methodology.
* `train_tinystories_patch_model.py`: The logic used for the fine-tuning process.
* *Note: Model weights (.pth) are excluded from this repo due to file size constraints.*






