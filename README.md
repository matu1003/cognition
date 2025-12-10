# Mental Rotation of Letters – Replicating Cooper & Shepard (1973)

**Short description.**  
This project implements a modern replication of the classic mental rotation experiment from **Cooper & Shepard (1973), “The time required to prepare for a rotated stimulus”** using the [Expyriment](https://www.expyriment.org) framework in Python. Participants decide whether a rotated letter “R” is normal or mirror-reversed while their reaction times are recorded as a function of rotation angle. :contentReference[oaicite:0]{index=0}

> 🔬 Goal: reproduce the characteristic increase in reaction time with angular deviation from upright, and explore how closely we can match the original patterns with a simple lab-style experiment.

![Example setup / mental rotation illustration](docs/hero_mental_rotation.png)

---

## Table of Contents

- [1. Background](#1-background)
- [2. Experimental design](#2-experimental-design)
- [3. Code structure](#3-code-structure)
- [4. Running the experiment](#4-running-the-experiment)
- [5. Data format & analysis](#5-data-format--analysis)
- [6. Example results](#6-example-results)
- [7. Roadmap](#7-roadmap)
- [8. Requirements & installation](#8-requirements--installation)
- [9. Citation](#9-citation)

---

## 1. Background

Cooper & Shepard (1973) showed that the time needed to decide whether a rotated alphanumeric character is normal or mirror-reversed **increases approximately linearly with the angle of rotation** away from the upright orientation. This finding is a cornerstone in the study of **mental imagery and mental rotation**, suggesting that people internally “rotate” a mental image of the stimulus. :contentReference[oaicite:1]{index=1}  

The original experiment used letters and digits presented at different orientations, with conditions manipulating how much advance information participants had about the upcoming stimulus.

This repository provides:

- a minimal, modern implementation of a **letter-rotation task** in Python/Expyriment, :contentReference[oaicite:2]{index=2}  
- tools to **collect data** locally,
- and a basic **analysis pipeline** to visualize reaction times (RTs) as a function of rotation angle and mirror vs. normal letters.

---

## 2. Experimental design

We implement a simplified version of the paradigm:

- **Stimulus**: the letter **“R”**, presented either in its normal form or mirror-reversed.
- **Rotations**:  
  `0°, 60°, 120°, 180°, 240°, 300°` (clockwise)
- **Conditions**:
  - `version = "normal"`  
  - `version = "mirror"`
- **Trials**:
  - 3 repetitions per (angle × version) combination  
    → total of 6 angles × 2 versions × 3 reps = **36 trials**
  - order **randomized** at the beginning of the experiment.
- **Timing** (configurable in `base.py`):
  - Fixation cross: 500 ms  
  - Optional cue (angle text): 400 ms (`SOA`)  
  - Maximum response window: 3000 ms  

**Task.**  
Participants press:
- **F** for *normal* “R”
- **J** for *mirror* “R”

The script records:

- trial index  
- rotation angle  
- version (normal / mirror)  
- pressed key  
- correctness (0 / 1)  
- reaction time (RT) in ms

---

## 3. Code structure

Main experiment script: [`base.py`](base.py). :contentReference[oaicite:3]{index=3}

Key parts:

- **Global parameters** (angles, versions, repetitions, timing)
- **Trial list construction and randomization**
- **Expyriment setup**:
  - `Experiment` object
  - fixation cross and blank screen
  - base stimulus for the letter “R”
- **Instructions screens**
- **Trial loop**:
  - inter-trial blank
  - fixation
  - creation of stimulus (normal or mirror + rotation)
  - optional text cue
  - stimulus presentation
  - keyboard response (`f` or `j`)
  - correctness computation
  - data logging via `exp.data.add(...)`
- **Experiment end** (saves `.xpd` data file)

You can use this file as a starting point and modify:

- the **set of letters**,
- the **angles**,  
- or add new conditions (e.g. manipulation of advance information as in the original paper).

---

## 4. Running the experiment

1. **Install dependencies** (see [Requirements](#8-requirements--installation)).
2. Plug in a keyboard and make sure the F and J keys are easily accessible.
3. Run:

   ```bash
   python base.py
