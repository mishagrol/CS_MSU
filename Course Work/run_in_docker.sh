#!/bin/bash
docker run --rm -p 8895:8895 -v $PWD:/home/ monica jupyter-notebook --no-browser --NotebookApp.token=SecretToken --port 8895 --ip 0.0.0.0 --allow-root
