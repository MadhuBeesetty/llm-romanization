# The Invisible Gap: Romanized Indic Generation Fails Where Automatic Metrics Succeed

[![arXiv](https://img.shields.io/badge/arXiv-2611.09085-b31b1b.svg)](https://arxiv.org/abs/2611.09085)
[![PDF](https://img.shields.io/badge/Paper-PDF-red.svg)](paper/The_Invisible_Gap.pdf)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Official repository for the paper:  
**"The Invisible Gap: Romanized Indic Generation Fails Where Automatic Metrics Succeed"**  
*Surbhi Sharma\*, Devesh Maheshwari\*, Lokesh Meesala\*, Madhu Sudhan Rao Beesetty\** (\*Equal contribution)

📄 **arXiv**: [https://arxiv.org/abs/2611.09085](https://arxiv.org/abs/2611.09085)  
📥 **Paper PDF**: [`paper/The_Invisible_Gap.pdf`](paper/The_Invisible_Gap.pdf)

---

## 📌 Abstract

Hundreds of millions of Indians communicate with digital systems in romanized Latin characters—typing *aap kaise hain* (आप कैसे हैं) rather than native script—yet romanized Indic generation is absent from NLP benchmarks and evaluation frameworks. We demonstrate that automatic metrics (BGE-M3, BERTScore) systematically misrepresent the quality of romanized Hindi, Telugu, and Kannada generation.

We evaluate four LLMs (**Claude Opus 4.8**, **GPT-5.5**, **Gemini 2.5-flash**, and **Qwen3.5-35B**) on 142 OpenAssistant query-response pairs. On a 72-response diagnostic subset, native speakers rate GPT-5.5 1.43 points higher than Claude Opus 4.8 on a 12-point rubric, whereas their full-dataset BGE-M3 means differ by only 0.004. Two distinct model-specific failure modes emerge:
1. **Script spillage**: Gemini produces script leakage (16.9% of Telugu responses leak native script).
2. **Instruction collapses**: Qwen collapses to English-only output (16.2% of Kannada responses).

We introduce a **failure-aware evaluation policy** that assigns zero to empty outputs, script-corrupted responses, and instruction collapses—revealing failures metrics alone cannot detect. Our results show that evaluating romanized Indic generation requires a coordinated bundle: semantic similarity, script compliance, failure coverage, and native-speaker acceptability.

---

## 🗂️ Repository Structure

```text
├── paper/
│   └── The_Invisible_Gap.pdf        # Complete final paper PDF
├── data/                            # Benchmark prompts & preprocessed splits
├── output/                          # Model generations & scored evaluation results
│   ├── anthropic_output/
│   ├── gemini/
│   ├── gpt/
│   ├── ollama/
│   └── figures/                     # BERTScore and BGE metric visualization plots
├── human-evaluation/                # Native speaker diagnostic subsets & rubric logs
├── scripts/                         # LLM inference & evaluation scripts
├── romanized_scoring_pipeline.py    # Pipeline to compute automated semantic metrics
├── get_score_summary.py             # Computes failure-aware metric summary tables
└── README.md
```

---

## 🚀 Quickstart

### 1. Environment Setup

Clone the repository and install the dependencies:

```bash
git clone https://github.com/MadhuBeesetty/llm-romanization.git
cd llm-romanization
pip install -r requirements.txt  # or install: pandas numpy bert-score sentence-transformers matplotlib
```

### 2. Compute Metric Summaries

To compute the failure-aware scoring summary across all model generations:

```bash
python get_score_summary.py
```

### 3. Generate Evaluation Figures

To reproduce the benchmark figures:

```bash
python scripts/plot_metrics.py
```

---

## 📝 Citation

If you find this work, dataset, or codebase useful in your research, please cite:

```bibtex
@article{sharma2026invisiblegap,
  title   = {The Invisible Gap: Romanized Indic Generation Fails Where Automatic Metrics Succeed},
  author  = {Sharma, Surbhi and Maheshwari, Devesh and Meesala, Lokesh and Beesetty, Madhu Sudhan Rao},
  journal = {arXiv preprint arXiv:2611.09085},
  year    = {2026},
  url     = {https://arxiv.org/abs/2611.09085}
}
```
