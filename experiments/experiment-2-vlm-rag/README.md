# Experiment 2 — VLM-Based Visual Diagnosis for RAG

## Objective

Evaluate whether replacing the current EfficientNet-B3 image classification
with a Vision-Language Model (VLM) for structured visual diagnosis improves
the quality of the downstream RAG-based agricultural recommendations.

## Research Question

Does VLM-based visual diagnosis provide a more useful representation of
irrigation problems for RAG-based recommendation generation compared with
classification-only visual input?

## Experimental Pipeline

### Baseline

Image
→ EfficientNet-B3
→ Problem Classification
→ Existing RAG Recommendation Service
→ Qwen2.5-7B
→ Recommendation

### Experiment 2

Image
→ Qwen3-VL-32B
→ Structured Visual Diagnosis
→ Query Builder
→ Existing RAG Recommendation Service
→ Qwen2.5-7B
→ Recommendation