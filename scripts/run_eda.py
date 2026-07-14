"""
Runner script for EDA.
Ensures the project root is in Python path, then calls the modular eda pipeline.
"""
import sys
import os

# Add the project root to Python path so 'src' can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.eda import run_full_analysis

if __name__ == "__main__":
    run_full_analysis()