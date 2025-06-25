# vivpro-take-home
This repository contains my solution for Vivpro's Backend Take Home assignment

---

## Overview:
This project aims to:
1. Normalize a nested JSON dataset of songs into a clean, tabular format.
2. Store this data for use in a backend API.
3. Provide API endpoints to:
   - Retrieve all songs.
   - Look up a song by title.

---

## Setup:
I like to use Chocolatey since I'm on a Windows machine. The steps to install chocolatey can be found [here](https://chocolatey.org/install).
1. In an elevated terminal, run the command `choco install python` (installs latest available package - use `choco install python --versionx.xx.x` if you need a specific version). It will ask if you want to run the script - enter `Y` to proceed.
2. After the installation is complete, run `python --version` to verify that it has been installed correctly.
3. Now, install the following packages for this project:
    
    i. pandas: `pip install pandas` <br>
    ii. pydantic: `pip install pydantic`

The environment should now be set up.

## Technical Description:

