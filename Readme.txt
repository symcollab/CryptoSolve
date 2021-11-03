# CryptoSolve

To install, run the following in the terminal at the root directory of the project:
```bash
./install.sh
source ~/.profile
```

To run our script that automatically generates modes of operations and checks for security do the following:
```bash
cd experiments
python3 moo_experiment.py
```
While this is running, you can check out the analysis of the MOOs checked by running the following:
```bash
python3 moo_analysis.py
```

Three of the MOOs in our paper, were thought of outside the MOO generator and checked using our custom MOO functionality.
To see, from the root directory:
```bash
cd examples
python3 custom_moo.py
```

You can checkout the web interface by running the following in the terminal
```bash
moo_website
```

You can checkout the terminal interface by running the following in the terminal
```bash
moo_tool
```


