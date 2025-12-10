#!/usr/bin/env python3
"""
Export all 527 AudioSet labels from AST model to analyze for filtering and merging
"""

from transformers import ASTForAudioClassification
import json

MODEL_NAME = "MIT/ast-finetuned-audioset-10-10-0.4593"

print(f"Loading model config: {MODEL_NAME}")
model = ASTForAudioClassification.from_pretrained(MODEL_NAME)

if hasattr(model.config, 'id2label'):
    id2label = model.config.id2label
    print(f"\nTotal labels: {len(id2label)}")

    # Export to JSON
    with open('all_labels.json', 'w', encoding='utf-8') as f:
        json.dump(id2label, f, indent=2, ensure_ascii=False)
    print("\nExported to: all_labels.json")

    # Print all labels sorted alphabetically
    print("\n" + "="*80)
    print("ALL LABELS (alphabetically sorted)")
    print("="*80)

    labels_sorted = sorted([(idx, label) for idx, label in id2label.items()],
                          key=lambda x: x[1].lower())

    for idx, label in labels_sorted:
        print(f"{idx:4s}: {label}")

else:
    print("Error: Labels not found in model config")
