import sys
import os

# Add root folder to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.multiple_value_scanner import MultipleValueScanner

def main():
    print("=" * 80)
    print("LANForge AI - Multi-Value Parameter Scanner (Ollama GPTOSS20B)")
    print("=" * 80)
    
    scanner = MultipleValueScanner()
    success = scanner.update_knowledge_base()
    
    if success:
        print("\n[SUCCESS] Scanning finished successfully. Run python server.py and reload Chrome to see updated picklist checkmarks!")
    else:
        print("\n[FAILED] Scanner execution encountered errors. Check logs above.")

if __name__ == "__main__":
    main()
