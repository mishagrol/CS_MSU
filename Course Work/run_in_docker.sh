#!/bin/bash
docker run --rm -p 8888:8888 -v $PWD:/home/ monica jupyter-notebook --no-browser --NotebookApp.token=SecretToken --port 8888 --ip 0.0.0.0 --allow-root
