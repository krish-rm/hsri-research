#!/usr/bin/env python3
"""
Script to run the complete Phase 3: Index Construction pipeline
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to Python path
project_root = Path.cwd()
sys.path.insert(0, str(project_root))

def run_normalization():
    """Run data normalization"""
    print("1. Running data normalization...")
    from scripts.data_normalization import DataNormalizer

    normalizer = DataNormalizer(project_root)
    if normalizer.run_normalization():
        print("   ✅ Normalization completed")
        return True
    else:
        print("   ❌ Normalization failed")
        return False

def run_validation():
    """Run statistical validation"""
    print("2. Running statistical validation...")
    from scripts.statistical_validation import StatisticalValidator

    validator = StatisticalValidator(project_root)
    if validator.run_validation():
        print("   ✅ Statistical validation completed")
        return True
    else:
        print("   ❌ Statistical validation failed")
        return False

def run_index_construction():
    """Run index construction"""
    print("3. Running index construction...")
    from scripts.index_construction import IndexConstructor

    constructor = IndexConstructor(project_root)
    if constructor.construct_index():
        print("   ✅ Index construction completed")
        return True
    else:
        print("   ❌ Index construction failed")
        return False

def main():
    """Run complete Phase 3 pipeline"""
    print("Starting HSRI-Proxy v0.1 Phase 3: Index Construction")
    print("=" * 50)

    # Run all steps
    steps = [
        run_normalization,
        run_validation,
        run_index_construction
    ]

    for step in steps:
        if not step():
            print("\n❌ Phase 3 pipeline failed!")
            return 1

    print("\n✅ Phase 3 completed successfully!")
    return 0

if __name__ == "__main__":
    exit(main())