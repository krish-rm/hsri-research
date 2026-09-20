#!/usr/bin/env python3
"""
Script to run the complete data normalization process for HSRI-Proxy v0.1
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path.cwd()
sys.path.insert(0, str(project_root))

from scripts.data_normalization import DataNormalizer

def main():
    """Run the normalization process"""
    print("Starting HSRI-Proxy v0.1 Data Normalization...")

    normalizer = DataNormalizer(project_root)

    if normalizer.run_normalization():
        print("\n✅ Normalization completed successfully!")
        return 0
    else:
        print("\n❌ Normalization failed!")
        return 1

if __name__ == "__main__":
    exit(main())