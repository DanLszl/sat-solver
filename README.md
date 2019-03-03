# sat-solver

## Requirements
Python 3.6

### To run the experiments and analyzing notebooks, also run (this is not needed for the SAT solver)

```pip install -r requirements.txt```

## Usage
Navigate to the folder of the repository and run:

```./SAT.py -Sn input_file```

Where n is a number between 0 and 7 specifying the heuristic to run. 
    
* S0: Basic Davis-Putnam algorithm 
* S1: DLCS 
* S2: MOM 
* S3: Jeroslaw-Wang 
* S4: Basic DP + biased coin flip 
* S5: DLCS + biased coin flip 
* S6: MOM + biased coin flip 
* S7: Jeroslaw-Wang + biased coin flip
