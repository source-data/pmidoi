# pmidoi
Extaction of pmid - doi relationship for a given journal using EuropePMC

Activate virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Test app:

    python -m test.tester

Install app:
    
    python -m setup install


Run the analysis for the journal with title "My Journal" and save the results as tab-delimted text into `destination.txt`:

    listids "My Journal" destination.txt
