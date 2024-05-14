<a name="readme-top"></a>

<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/python-logo-master-v3.png" alt="Logo" width=400>
  </a>

<h3 align="center">Analog Designer</h3>
  <p align="center">
    A CLI for designing pre-modelled analog circuits.
    <br />
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#how-it-works">How it Works</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

## About The Project

Written as part of my Bsc thesis during spring 2024 to help with the design of a small handful of common opamp configurations. The tool takes transistor models created with [SPICE](https://en.wikipedia.org/wiki/SPICE) and is designed to be used with the [gm/id method](http://web02.gonzaga.edu/faculty/talarico/EE406/documents/gmid.pdf).

## Getting Started

If you're interested in using this useful (but really rather limited) tool, you can do the following.

### Prerequisites

The only dependency is Numpy which can be installed using pip

   ```sh
   pip install numpy
   ```

### Installation

Clone this repo by

   ```sh
   git clone https://github.com/Ponti17/analog-designer.git
   ```

## How it Works

The SPICE generated transistor models are placed in `/models`. The DataHandler class described in `_datahandler.py` is capable of loading and parsing these models, as well as fetching relevant information. The MosDevice class described in `transistor.py` models a basic N- or PMOS transistor. A MosDevice object can be defined and need the followwing:

- **Model:** For example "pch", "nvh", "nvh_lvt" etc.
- **Length:** The gate length of the device, called gateL.
- **VDS:** The drain source voltage (called vdsrc) affects the small signal output resistance and is required for accurate calculations.
- **gm/ID:** A chosen gm/ID operating point. Perhaps chosen using the [analog-explorer](https://github.com/Ponti17/analog-explorer.git).

Currently the tool supports three common op-amp configurations:

- Three-mirror OTA (described in ota.py)
- Simple two-stage w/ pmos LTP and full-swing output stage (described in twostage.py)
- High input-swing folded cascode (described in foldedcascode.py)

The amplifiers are defined as classes and has relevant MosDevices defined. When possible symmetry is assumed to simplify modelling. Each amplifiers has methods such as **av** (open-loop gain), **rout**, **poles** etc.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>