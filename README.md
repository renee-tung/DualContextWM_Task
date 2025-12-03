# Dual Context Working Memory (DCWM) Task

## Overview

The Dual Context Working Memory (DCWM) Task presents participants with visual stimuli and verbal instructions about image choice and response type. Based on the instructions, participants will choose one of the images, and respond with either a button press or slider. The task supports both training and main experimental versions.


## Files

### Main Scripts
- `main.py` - Main script for the experimental task
- `main_training.py` - Main script for the training version

### Core Functions
- `init_task.py` - Initialize task parameters and display for main task
- `init_task_training.py` - Initialize task parameters for training
- `run_session.py` - Run the experimental session (main task)
- `run_session_training.py` - Run the training session
- `finish_experiment.py` - Clean up after main experiment
- `finish_experiment_training.py` - Clean up after training

### Relevant Helper Functions
- `get_instruction_text.py` - Generate instruction text based on trial parameters
- `get_motor_instruction_text.py` - Generate response text (button/slider) based on trial parameters
- `get_correct_responses.py` - Calculate correct responses for trials
- `get_correct_responses_training.py` - Calculate correct responses for training trials
- `intermission_screen.py` - Display intermission/break screens
- `send_blackrock_comment.py` - Send comments to Blackrock machine
- `cbmex_utils.py` - Utils functions from Baylor to assist with Blackrock comments
- `photodiode_utils.py` - Utils functions to refresh photodiode for timing
- `filter_picklable.py` - Function for saving relevant data at the end of each trial

### Stimuli
- `Task_Stim_New_v1` - relevant folder for task stimuli
- `Training` = relevant folder for training stimuli

### Instructions
- `DCWM_Instructions.docx` - word doc with relevant instructions for running task
- `DCWM_Instructions.pptx` - powerpoint accompanying the word document
- `DCWM_Task_Parameters.xlsx` - not instructions, but may be helpful to understand task blocks

## Requirements

### Python Packages
- Install via environment.yml file

### Hardware Support
- **Cerebus**: For Blackrock connection (cbmex_utils)

## Usage

### Running the Main Task
```bash
python main.py
```

### Running the Training Version
```bash
python main_training.py
```

## Configuration

### Debug Mode
Select debug = 1 when prompted to:
- Skip Blackrock comment sending
- Use smaller window size
- Bypass sync tests

### Input Devices
- **Keyboard**: Default input method (Left/Right arrow keys)


## Data Output

Data is saved as pickle files in:
- Main task: `../patientData/taskLogs/`
- Training: `../patientData/trainingLogs/`

Neural data logs will be saved in: 
- Main task: `../patientData/neuralLogs/`
- Training: `../patientData/neuralLogs_training/`

Each file contains:
- `task_struct`: All task parameters and trial data
- `disp_struct`: Display configuration

## License

This code built off of a task written by Tomas Aquino in PsychToolbox, found here: https://github.com/43technetium/VerbalInstructionTask

