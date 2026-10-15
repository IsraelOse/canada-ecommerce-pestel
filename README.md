# Canada E-commerce PESTEL Analysis

A data-driven **PESTEL** (Political, Economic, Social, Technological, Environmental, Legal) analysis of the Canadian e-commerce market, backed by a reproducible data pipeline that consolidates public macro indicators.

## What it does
- Collects and harmonises macro indicators relevant to e-commerce: Consumer Confidence Index, CPI, household consumption, internet usage, mobile subscriptions, population/urban population, and retail e-commerce sales (2017–2026)
- A Python pipeline (`PESTEL_Data_Pipeline.ipynb`) merges them into a single consolidated, monthly dataset
- Findings synthesised into an analytical report and presentation

## Repo layout
| Path | What it is |
|------|-----------|
| `PESTEL_Data_Pipeline.ipynb` | Data-collection & consolidation pipeline |
| `PESTEL_Data_Pipeline_executed.ipynb` | Executed version with outputs |
| `Consolidated_PESTEL_Dataset.csv` / `.xlsx` | Final merged dataset |
| `raw_indicators/` | Source indicator files |
| `Part1_Data_Collection_Description.docx` | Methodology |
| `PESTEL_Analytical_Report.docx` | Analytical report |
| `PESTEL_Presentation.pptx` | Slide deck |

## Tech
Python · pandas · openpyxl

> **Academic group project (Group 6)**, DAMO-501 Data Analytics Case Study. Shared coursework; teammate contributions acknowledged. _Add teammate names here._
