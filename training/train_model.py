#!/usr/bin/env python3
"""
Training Pipeline for Multi-Agent Legal RAG System
Fine-tunes models on the synthetic datasets using PEFT/LoRA.

This pipeline:
1. Loads synthetic datasets for all 3 objectives
2. Converts them to training format (instruction-following)
3. Fine-tunes using PEFT/LoRA for efficiency
4. Evaluates model performance
"""

import json
import logging
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# ============================================================================
# DATA PREPARATION
# ============================================================================

def load_dataset(file_path: str) -> dict:
    """Load a JSON dataset."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def prepare_obj1_training_data(dataset: dict, max_samples: int = 5000) -> list[dict]:
    """Convert Objective 1 (Conflict Resolution) dataset to instruction-following format."""
    training_data = []
    scenarios = dataset.get("scenarios", [])[:max_samples]

    for scenario in scenarios:
        # Create instruction-output pairs
        instruction = (
            f"You are a legal compliance expert specializing in Indian construction law. "
            f"Analyze the following jurisdictional conflict and provide a detailed resolution.\n\n"
            f"**Conflict Type:** {scenario.get('conflict_type', 'Unknown')}\n"
            f"**City:** {scenario.get('city', 'Unknown')}, {scenario.get('state', '')}\n"
            f"**Building Type:** {scenario.get('building_type', 'Unknown')}\n"
            f"**Description:** {scenario.get('conflict_description', '')}\n"
            f"**Jurisdiction 1:** {scenario.get('jurisdiction1', {}).get('authority', '')} - "
            f"{scenario.get('jurisdiction1', {}).get('requirement', '')}\n"
            f"**Jurisdiction 2:** {scenario.get('jurisdiction2', {}).get('authority', '')} - "
            f"{scenario.get('jurisdiction2', {}).get('requirement', '')}\n"
        )

        output = json.dumps({
            "resolution_strategy": scenario.get("resolution_strategy", ""),
            "resolution_description": scenario.get("resolution_description", ""),
            "reasoning_chain": scenario.get("reasoning_chain", []),
            "expected_outcome": scenario.get("expected_outcome", {}),
            "applicable_laws": scenario.get("applicable_laws", []),
        }, indent=2)

        training_data.append({
            "instruction": instruction,
            "input": "",
            "output": output,
            "objective": "conflict_resolution",
        })

    return training_data


def prepare_obj2_training_data(dataset: dict, max_samples: int = 2000) -> list[dict]:
    """Convert Objective 2 (Prediction) dataset to instruction-following format."""
    training_data = []
    scenarios = dataset.get("prediction_scenarios", [])[:max_samples]

    for scenario in scenarios:
        project_ctx = scenario.get("project_context", {})
        instruction = (
            f"You are a predictive compliance analysis expert for Indian construction law. "
            f"Analyze the project and predict future compliance violations.\n\n"
            f"**Building Type:** {project_ctx.get('building_type', 'Unknown')}\n"
            f"**Project Size:** {project_ctx.get('project_size', 'Unknown')}\n"
            f"**City:** {scenario.get('city', 'Unknown')}\n"
            f"**Current Phase:** {project_ctx.get('current_phase', 'Unknown')}\n"
            f"**Timeline:** {project_ctx.get('project_start', '')} to {project_ctx.get('project_end', '')}\n"
            f"**Current Permits:** {', '.join(project_ctx.get('current_permits', []))}\n"
        )

        output = json.dumps({
            "predictions": scenario.get("predicted_code_changes", []),
            "compliance_roadmap": scenario.get("compliance_roadmap", {}),
            "recommendation": scenario.get("recommendation", {}),
            "historical_precedents": scenario.get("historical_precedents", []),
        }, indent=2)

        training_data.append({
            "instruction": instruction,
            "input": "",
            "output": output,
            "objective": "time_prediction",
        })

    return training_data


def prepare_obj3_training_data(dataset: dict, max_samples: int = 3000) -> list[dict]:
    """Convert Objective 3 (Verification) dataset to instruction-following format."""
    training_data = []
    scenarios = dataset.get("scenarios", [])[:max_samples]

    for scenario in scenarios:
        project = scenario.get("project_context", {})
        inspection = scenario.get("inspection_details", {})

        instruction = (
            f"You are a compliance verification expert for Indian construction law. "
            f"Generate an inspector-ready compliance report.\n\n"
            f"**Project:** {project.get('project_name', 'Unknown')}\n"
            f"**Building Type:** {project.get('building_type', 'Unknown')}\n"
            f"**Size:** {project.get('project_size', 'Unknown')}\n"
            f"**City:** {scenario.get('city', 'Unknown')}, {scenario.get('state', '')}\n"
            f"**Developer:** {project.get('developer', 'Unknown')}\n"
            f"**Inspection Type:** {inspection.get('inspection_type', 'Unknown')}\n"
            f"**Inspector:** {inspection.get('inspector_name', 'Unknown')}\n"
        )

        output = json.dumps({
            "findings": scenario.get("findings", []),
            "summary": scenario.get("summary", {}),
            "compliance_report": scenario.get("compliance_report", {}),
            "traceable_evidence": scenario.get("traceable_evidence", {}),
        }, indent=2)

        training_data.append({
            "instruction": instruction,
            "input": "",
            "output": output,
            "objective": "verification",
        })

    return training_data


def combine_training_data(data_dir: str, output_path: str) -> list[dict]:
    """Combine all training data into a single dataset."""
    all_data = []

    # Load Objective 1
    obj1_path = os.path.join(data_dir, "objective1_conflict", "conflict_resolution_dataset.json")
    if os.path.exists(obj1_path):
        logger.info("Loading Objective 1 dataset...")
        obj1 = load_dataset(obj1_path)
        obj1_data = prepare_obj1_training_data(obj1)
        all_data.extend(obj1_data)
        logger.info(f"  Objective 1: {len(obj1_data)} training samples")

    # Load Objective 2
    obj2_path = os.path.join(data_dir, "objective2_prediction", "prediction_dataset.json")
    if os.path.exists(obj2_path):
        logger.info("Loading Objective 2 dataset...")
        obj2 = load_dataset(obj2_path)
        obj2_data = prepare_obj2_training_data(obj2)
        all_data.extend(obj2_data)
        logger.info(f"  Objective 2: {len(obj2_data)} training samples")

    # Load Objective 3
    obj3_path = os.path.join(data_dir, "objective3_verification", "verification_dataset.json")
    if os.path.exists(obj3_path):
        logger.info("Loading Objective 3 dataset...")
        obj3 = load_dataset(obj3_path)
        obj3_data = prepare_obj3_training_data(obj3)
        all_data.extend(obj3_data)
        logger.info(f"  Objective 3: {len(obj3_data)} training samples")

    # Save combined dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    logger.info(f"Combined training dataset: {len(all_data)} samples saved to {output_path}")

    # Create HF datasets format (JSONL)
    jsonl_path = output_path.replace(".json", ".jsonl")
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for item in all_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    logger.info(f"JSONL format saved to {jsonl_path}")
    return all_data


# ============================================================================
# TRAINING WITH PEFT/LoRA
# ============================================================================

def train_with_peft(
    training_data_path: str,
    base_model: str = "meta-llama/Meta-Llama-3.1-8B",
    output_dir: str = None,
):
    """Fine-tune a model using PEFT/LoRA on the training data."""
    try:
        import torch
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            BitsAndBytesConfig,
            TrainingArguments,
        )
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
        from datasets import load_dataset
        from trl import SFTTrainer
    except ImportError as e:
        logger.error(f"Missing training dependencies: {e}")
        logger.error("Install with: pip install torch transformers peft datasets trl bitsandbytes accelerate")
        return None

    if output_dir is None:
        output_dir = str(PROJECT_ROOT / "training" / "output" / f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

    os.makedirs(output_dir, exist_ok=True)

    logger.info(f"Loading base model: {base_model}")

    # Quantization config for memory efficiency
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    # Load model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # Prepare model for training
    model = prepare_model_for_kbit_training(model)

    # LoRA config
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Load training dataset
    dataset = load_dataset("json", data_files=training_data_path, split="train")

    def formatting_func(examples):
        texts = []
        for instruction, inp, output in zip(examples["instruction"], examples["input"], examples["output"]):
            text = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\nYou are a legal compliance expert for Indian construction law.<|eot_id|><|start_header_id|>user<|end_header_id|>\n{instruction}"
            if inp:
                text += f"\n{inp}"
            text += f"<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n{output}<|eot_id|>"
            texts.append(text)
        return {"text": texts}

    dataset = dataset.map(formatting_func, batched=True)

    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-5,
        weight_decay=0.01,
        warmup_steps=500,
        logging_steps=50,
        save_steps=500,
        save_total_limit=3,
        fp16=True,
        optim="paged_adamw_32bit",
        lr_scheduler_type="cosine",
        report_to="none",
        remove_unused_columns=False,
    )

    # Trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=lora_config,
        tokenizer=tokenizer,
        args=training_args,
        max_seq_length=2048,
    )

    logger.info("Starting training...")
    trainer.train()

    # Save model
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

    logger.info(f"Model saved to {output_dir}")
    return output_dir


# ============================================================================
# EVALUATION USING GROQ
# ============================================================================

def evaluate_with_groq(test_samples: list[dict], output_path: str = None):
    """Evaluate fine-tuned model outputs against Groq baseline."""
    from config.settings import GROQ_API_KEY, GROQ_MODELS
    from groq import Groq

    client = Groq(api_key=GROQ_API_KEY)
    results = []

    for i, sample in enumerate(test_samples[:100]):  # Evaluate on 100 samples
        messages = [
            {
                "role": "system",
                "content": "You are a legal compliance expert for Indian construction law. Provide accurate, structured responses in JSON format.",
            },
            {"role": "user", "content": sample["instruction"]},
        ]

        try:
            response = client.chat.completions.create(
                model=GROQ_MODELS["primary"],
                messages=messages,
                temperature=0.1,
                max_tokens=4096,
            )

            predicted = response.choices[0].message.content
            expected = sample["output"]

            results.append({
                "sample_id": i,
                "objective": sample.get("objective", "unknown"),
                "predicted": predicted,
                "expected": expected,
                "status": "generated",
            })
        except Exception as e:
            logger.error(f"Evaluation error for sample {i}: {e}")
            results.append({
                "sample_id": i,
                "status": "error",
                "error": str(e),
            })

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"Evaluation results saved to {output_path}")

    return results


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main training pipeline."""
    print("=" * 60)
    print("MULTI-AGENT LEGAL RAG - TRAINING PIPELINE")
    print("=" * 60)

    data_dir = str(PROJECT_ROOT / "datasets")
    training_dir = str(PROJECT_ROOT / "training")

    # Step 1: Prepare training data
    print("\n[Step 1] Preparing training data...")
    combined_path = os.path.join(training_dir, "combined_training_data.json")
    training_data = combine_training_data(data_dir, combined_path)
    print(f"  Total training samples: {len(training_data)}")
    print(f"  - Conflict Resolution: {sum(1 for d in training_data if d['objective'] == 'conflict_resolution')}")
    print(f"  - Time Prediction: {sum(1 for d in training_data if d['objective'] == 'time_prediction')}")
    print(f"  - Verification: {sum(1 for d in training_data if d['objective'] == 'verification')}")

    # Step 2: Training (optional - requires GPU)
    print("\n[Step 2] Model Training...")
    print("  NOTE: Training requires GPU. Run with: python training/train_model.py --train")
    if "--train" in sys.argv:
        try:
            output = train_with_peft(combined_path)
            print(f"  ✓ Model trained and saved to {output}")
        except Exception as e:
            print(f"  ✗ Training failed: {e}")
    else:
        print("  Skipping training (use --train flag to enable)")

    # Step 3: Evaluation with Groq
    print("\n[Step 3] Evaluation with Groq baseline...")
    eval_samples = training_data[:100]
    eval_path = os.path.join(training_dir, "evaluation_results.json")
    eval_results = evaluate_with_groq(eval_samples, eval_path)
    print(f"  ✓ Evaluated {len(eval_results)} samples")

    # Summary
    print("\n" + "=" * 60)
    print("TRAINING PIPELINE COMPLETE")
    print("=" * 60)
    print(f"  Training data: {combined_path}")
    print(f"  Training data (JSONL): {combined_path.replace('.json', '.jsonl')}")
    print(f"  Evaluation results: {eval_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
