morphology-synthesis-api
========================

Single cell topological synthesis service.

Build & Run
===========

Build morphology-sythesis-api docker image:

.. code-block:: bash

    docker build -t morphology-synthesis-api . \
    --build-arg PROJECT_PATH=morphology-synthesis-api:local \
    --build-arg COMMIT_SHA=$(git rev-parse HEAD)

And run:

.. code-block:: bash

    docker run --rm --name morphology-synthesis-api -p8000:8000 \
    -e DEBUG=true -e LOGGING_LEVEL=DEBUG \
    --cap-add SYS_PTRACE \
    morphology-synthesis-api

Example payload:

.. code-block: bash


Usage
=====

/synthesis-with-files
---------------------

/synthesis-with-files route allows synthesizing a cell morphology passing file paths in the POST request:

.. code-block:: bash

    curl -H 'Content-Type: application/json' \
         -X POST \
         -d '{"files": {"parameters_file": "tests/data/bio_rat_L5_TPC_B_parameters.json", "distributions_file":"tests/data/bio_rat_L5_TPC_B_distribution.json"}, "overrides":{"apical_dendrite":{"total_extent":10.0,"randomness":0.001, "orientation":[0.0, 0.0, 1.0], "step_size":1.0, "radius":0.5}}}' \
         http://0.0.0.0:8000/synthesis-with-files

/synthesis-with-resources
-------------------------

/synthesis-with-files on the other hand allows to specify NEXUS resource ids instead of local files to extract the topological parameters and distributions from.

.. code-block:: bash

    curl -H 'Content-Type: application/json' \
         -H 'nexus-token: ${NEXUS_TOKEN}'
         -X POST \
         -d '{"resources": {"parameters_file": "${PARAMETERS_ID}", "distributions_file":"${DISTRIBUTIONS_ID}"}, "overrides":{"apical_dendrite":{"total_extent":10.0,"randomness":0.001, "orientation":[0.0, 0.0, 1.0], "step_size":1.0, "radius":0.5}, "nexus_config": {"bucket": "${ORG}/${PROJ}", "endpoint": ${NEXUS_INSTANCE_ENDPOINT}}}}' \
         http://0.0.0.0:8000/synthesis-with-resources


Tests
=====

.. code-block:: bash

    pip install tox
    tox

Acknowledgements
================

The development of this software was supported by funding to the Blue Brain Project, a research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government’s ETH Board of the Swiss Federal Institutes of Technology.

For license and authors, see LICENSE.txt and AUTHORS.txt respectively.

Copyright (c) 2024 Blue Brain Project/EPFL
