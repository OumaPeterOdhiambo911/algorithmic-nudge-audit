# 🧠 Algorithmic Nudge Audit: Quantifying Ethical Costs in UI/UX

This project implements a framework to audit digital platform features that subtly manipulate user decisions (known as 'nudges'), focusing on the trade-off between **platform optimization** and **user autonomy**.

## 🏛️ Project Goal

To develop a quantitative scoring model and visualization tool to expose how interface elements are optimized to exploit user psychology rather than promote rational, long-term choice.

## 🛠️ Key Components

1.  **Data Simulation:** Generates hypothetical A/B test data where one group (`Test_Group=B`) is exposed to a design that increases conversion but compromises comprehension.
2.  **Autonomy Scoring:** Calculates a **Nudge Autonomy Deficit (NAD)** score based on interface variables (e.g., Opt-Out Difficulty, Urgency Messaging). A high NAD score indicates a more coercive design.
3.  **Ethical Trade-Off Visualization:** A bar chart comparing the percentage increase in the platform's desired outcome (e.g., subscription uptake) against the measured drop in user comprehension (the ethical cost).

## 🚀 How to Run

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-link]
    cd algorithmic-nudge-audit
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Execute the audit:**
    ```bash
    python audit_framework.py
    ```

The script will print the average NAD scores for both groups and display the ethical trade-off chart.
