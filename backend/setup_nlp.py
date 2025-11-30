import subprocess
import sys
import os

def install_spacy_model():
    """Download spaCy English model"""
    try:
        print("Downloading spaCy English model...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("spaCy model downloaded successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to download spaCy model: {e}")
        print("Application will work with reduced NLP capabilities")
        return False
    except FileNotFoundError:
        print("spaCy not found. Please install requirements first: pip install -r requirements.txt")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    try:
        print("Downloading NLTK data...")
        import nltk

        datasets = ['punkt', 'stopwords', 'averaged_perceptron_tagger', 'wordnet']
        for dataset in datasets:
            try:
                nltk.download(dataset, quiet=True)
                print(f"Downloaded NLTK {dataset}")
            except Exception as e:
                print(f"Could not download NLTK {dataset}: {e}")
        
        print("NLTK data setup complete!")
        return True
    except ImportError:
        print("NLTK not found. Please install requirements first: pip install -r requirements.txt")
        return False

def main():
    """Main setup function"""
    print("Setting up NLP dependencies for Skill Gap Predictor...")
    print("=" * 60)
 
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Virtual environment detected")
    else:
        print("No virtual environment detected. Consider using one.")
    
    success_count = 0

    if download_nltk_data():
        success_count += 1

    if install_spacy_model():
        success_count += 1
    
    print("=" * 60)
    if success_count == 2:
        print("All NLP dependencies set up successfully!")
        print("Your Skill Gap Predictor is ready to use with full NLP capabilities.")
    elif success_count == 1:
        print("Partial setup completed. Some NLP features may have reduced performance.")
        print("The application will still work with basic text processing.")
    else:
        print("Setup failed. Please check error messages above.")
        print("The application will fall back to basic keyword matching.")
    
    print("\n Next steps:")
    print("1. Copy .env.example to .env: cp .env.example .env")
    print("2. Start the application: python main.py")
    print("3. The API will be available at http://localhost:8000")

if __name__ == "__main__":
    main()