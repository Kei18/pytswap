# pytswap

[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](./LICENCE.txt)
[![CI](https://github.com/Kei18/pytswap/actions/workflows/ci.yml/badge.svg)](https://github.com/Kei18/pytswap/actions/workflows/ci.yml)

A minimal Python implementation of the TSWAP algorithm for unlabeled multi-agent pathfinding (aka. anonymous MAPF; AMAPF).
- Okumura, K. & Défago, X. Solving simultaneous target assignment and path planning efficiently with time-independent execution. AIJ. 2023. [[project-page]](https://kei18.github.io/tswap/)
  (best student paper award at ICAPS-22 🏆)

![](./assets/logo.gif)

TSWAP is a polynomial time, suboptimal, complete algorithm for solving unlabeled MAPF efficiently.
Just as [pypibt](https://github.com/Kei18/pypibt) for [PIBT](https://kei18.github.io/pibt2/), [pylacam](https://github.com/Kei18/py-lacam) for [LaCAM](https://kei18.github.io/lacam-project/), I here provide a distilled implementation.
In particular, the implementation is based on Algorithm 1 from the AIJ paper (not optimised one), and the scipy linear-sum optimal target assignment is adopted, although this is a bit slow for cost table preparation).
Please note that this remains a toy implementation designed to help you understand the algorithm. I do not think it is a good idea to use this implementation for benchmarking.

## Setup

This repository is setup with [uv](https://docs.astral.sh/uv/).
After cloning this repo, run the following to complete the setup.

```sh
uv sync
```

## Demo

```sh
uv run python app.py -m assets/empty_48_128.map -i assets/empty_48_128.scen -N 100
```

The result will be saved in `output.txt`
The grid maps and scenarios in `assets/` are from [MAPF benchmarks](https://movingai.com/benchmarks/mapf/index.html).

### Visualization

You can visualize the planning result with [@kei18/mapf-visualizer](https://github.com/kei18/mapf-visualizer).

```sh
mapf-visualizer ./assets/empty_48_128.map ./output.txt
```

![](./assets/demo.gif)

### Jupyter lab

Jupyter Lab is also available.
Use the following command:

```sh
uv run jupyter lab
```

You can see an example in `notebooks/demo.ipynb`.


## Licence

This software is released under the MIT License, see [LICENSE.txt](LICENCE.txt).
