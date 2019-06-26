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

Example:

```
$ listids "Molecular Systems Biology" msb.txt

total: 1086 | page: 1 from 2   
total: 1086 | page: 2 from 2   


Extracted ids from 1086 articles:

- 0 with no doi
- 19 with no pmid
- 0 with no doi and no pmid
- 1067 with both pmid and doi

Results saved to msb.txt.
```
