# Real-Time Embedded Systems Experiments

Python multicore scheduling simulations and a desktop visualizer, plus MATLAB fixed-point and filter experiments.

Coursework by **Ali Amiri**, Sharif University of Technology. Semester 8 — Embedded Systems.

## Scheduler

Install the plotting dependency with `pip install -r requirements.txt`.

```bash
cd scheduler
python simulation.py
```

`input.txt` is a newly supplied demonstration input: simulation duration and core count, then the number of tasks, then `name execution period deadline` per task. The script compares RM, DM, and EDF and writes schedules and a Gantt chart in its working directory.

Run `python scheduler/application.py` to open the Tkinter visualizer. It offers RMA, EDF, and a combined ordering, task/resource inputs, utilization summaries, and Gantt charts. Resource overlays are visual aids; formal resource-locking protocol correctness is not claimed.

## Fixed-point exercises

`matlab/` retains the original independent scripts for filter representations and fixed-point comparisons. MATLAB with the relevant Signal Processing / DSP / Fixed-Point functionality is required. Python syntax and example execution are checked separately from MATLAB and GUI behavior.

## Scope and attribution

This repository is a curated coursework archive. Original exercise structure and existing credits are retained; course-provided interfaces and testbenches may be present. Bundled textbooks, assignment PDFs, vendor IP implementations, binaries, and IDE caches are excluded. No blanket open-source license has been added to material with mixed course provenance.

See `VALIDATION.md` for checks and known limits.
