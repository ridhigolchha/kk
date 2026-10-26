# Lead Generation Tool

A lightweight, high-level lead generation utility for outbound sales and growth teams.

## Features

- Score leads based on fit, intent, source, and buying signals
- Generate realistic sample lead lists for campaigns
- Export leads as CSV for CRM import
- Run from a simple CLI

## Quick start

```bash
python leadgen.py --count 10 --output leads.csv --show
```

This generates a batch of leads, prints a short summary, and writes the CSV file.

## Python usage

```python
from leadgen import LeadGenerator

generator = LeadGenerator()
leads = generator.generate_batch(5)
print(leads)

with open('leads.csv', 'w', newline='', encoding='utf-8') as csv_file:
    generator.export_csv(leads, csv_file)
```

## Lead scoring model

The score is designed to approximate lead quality, including:

- industry fit
- job-title authority
- source quality
- budget readiness
- pain-point alignment

Scores range from 0 to 100, where higher values indicate stronger buying intent.
