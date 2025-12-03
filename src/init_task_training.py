"""
This function sets up screen display and task structs for training version.
"""

import numpy as np
import random
from datetime import datetime
from pathlib import Path
from psychopy import visual, monitors, event
from psychopy.hardware import keyboard

from src.get_instruction_text import get_instruction_text
from src.get_motor_instruction_text import get_motor_instruction_text
from src.get_correct_responses_training import get_correct_responses_training
# from init_cedrus import init_cedrus  # Commented out - using keyboard only

def init_task_training():
    """
    Initialize task and display structures for training.
    
    Returns:
    --------
    task_struct : dict
        Dictionary containing all task parameters
    disp_struct : dict
        Dictionary containing display parameters and window handles
    """
    # Some initial global setup
    np.random.seed()
    
    # Get user input
    sub_id = input('Participant number (sub-XXX):\n')
    blackrock_enabled = int(input('Blackrock comments enabled? 0=no, 1=yes:\n'))
    # eye_link_mode = int(input('Use Eyelink? 0=no, 1=yes:\n'))
    eye_link_mode = 0  # Always no Eyelink
    # use_cedrus = int(input('Use CEDRUS? 0=no, 1=yes:\n'))  # Commented out - using keyboard only
    use_cedrus = 0  # Always use keyboard (arrow keys)
    debug = int(input('Debug mode? 0=no, 1=yes:\n'))
    
    # Output folder
    output_folder = Path('..') / 'patientData' / 'trainingLogs'
    output_folder.mkdir(parents=True, exist_ok=True)
    
    file_name = f"{sub_id}_{datetime.now().strftime('%m-%d-%Y_%H-%M-%S')}"
    
    # Setting up task variables
    n_blocks = 1
    n_trials_per_block = 16
    n_trials = n_trials_per_block * n_blocks
    
    # Relevant axis of each trial
    category_names = ['Animals', 'Cars', 'Faces', 'Fruits']
    axis_names = [
        ['Colorful', 'Count'],
        ['New', 'Colorful'],
        ['New', 'Geometry'],
        ['Count', 'Geometry']
    ]
    category_and_axis = [category_names, axis_names]
    
    # Which of the two axes belonging to each category will be used in each trial
    trial_categories = [0, 1, 2, 3] 
    trial_axis = [0, 1]
    stim_pairs = [0] # only 1 pair per category/axis
    prompt_variants = [0, 1] # only use 1 prompt variant for training
    response_variants = [0, 1] # button choice vs slider
    cue_variants = [2, 1] # retrocue vs cue
    
    # just do 0 1 2 3 0 1 2 3 ... for categories
    trial_categories = [0, 1, 2, 3, 1, 2, 0, 3, 0, 1, 2, 3, 0, 1, 2, 3]
    # show all axes equally
    trial_axis = [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0]
    # only one stim pair per category/axis
    stim_pairs = [0] * n_trials
    # just use 1 prompt variant
    prompt_variants = [0] * n_trials
    # 4 button, 4 slider, then random
    response_variants = [0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0]
    # first half cue, second half retrocue
    cue_variants = np.array([1] * (n_trials_per_block // 2) + [2] * (n_trials_per_block // 2))
    
    
    # Determining which stimuli to use in each trial
    stim_folder = Path('..') / 'stimuli' / 'Training'
    trial_stims = [[None, None] for _ in range(n_trials)]
    trial_pairs = np.zeros(n_trials, dtype=int)
    stim1_position = np.full(n_trials, np.nan)
    stim2_position = np.full(n_trials, np.nan)
    break_trial = np.zeros(n_trials, dtype=int)
    
    # Response prompts
    prompt_types = [random.randint(1, 2) for _ in range(n_trials)]
    left_text = [None] * n_trials
    right_text = [None] * n_trials
    trial_instructions = [None] * n_trials
    response_instructions = [None] * n_trials
    
    # Trial loop to set up stimuli and instructions
    for t_i in range(n_trials):
        axis = trial_axis[t_i]
        category = trial_categories[t_i]
        stim_pair = stim_pairs[t_i]
        
        # Loading stimuli
        trial_folder = stim_folder / category_names[category] 
        folder_images = list(trial_folder.glob('*.jpg'))
        if len(folder_images) == 0:
            folder_images = list(trial_folder.glob('*.JPG'))
        
        sampled_images = random.sample(folder_images, min(2, len(folder_images)))
        trial_stims[t_i][0] = str(sampled_images[0])
        trial_stims[t_i][1] = str(sampled_images[1]) if len(sampled_images) > 1 else str(sampled_images[0])
        
        stim1_position[t_i] = 3
        stim2_position[t_i] = 3
        
        if (t_i + 1) % n_trials_per_block == 0 and t_i < n_trials - 1:
            break_trial[t_i] = 1
        
        # Instructions
        trial_axis_name = axis_names[category][axis]
        trial_instructions[t_i] = get_instruction_text(
            category, trial_axis_name, prompt_variants[t_i],
        )

        response_instructions[t_i] = get_motor_instruction_text(
            response_variants[t_i]
        )
        
        # Response prompts
        if prompt_types[t_i] == 1:
            left_text[t_i] = 'First'
            right_text[t_i] = 'Second'
        else:
            left_text[t_i] = 'Second'
            right_text[t_i] = 'First'

    # create time jitters
    fixations = np.random.uniform(0.9, 1.2, n_trials).round(3)
    delays = np.random.uniform(2, 2.4, n_trials).round(3)
    
    # Create task struct
    task_struct = {
        'sub_id': sub_id,
        'blackrock_enabled': bool(blackrock_enabled),
        'eye_link_mode': bool(eye_link_mode),
        'use_cedrus': bool(use_cedrus),
        'debug': bool(debug),
        'output_folder': output_folder,
        'file_name': file_name,
        'n_blocks': n_blocks,
        'n_trials_per_block': n_trials_per_block,
        'n_trials': n_trials,
        'trial_cues': cue_variants,
        'category_names': category_names,
        'axis_names': axis_names,
        'category_and_axis': category_and_axis,
        'trial_categories': trial_categories,
        'trial_axis': trial_axis,
        'prompt_variants': prompt_variants,
        'response_variants': response_variants,
        'trial_instructions': trial_instructions,
        'response_instructions': response_instructions, 
        'prompt_types': prompt_types,
        'stim_folder': stim_folder,
        'trial_stims': trial_stims,
        'trial_pairs': stim_pairs,
        'stim1_position': stim1_position,
        'stim2_position': stim2_position,
        'break_trial': break_trial,
        'left_text': left_text,
        'right_text': right_text,
        'fixation_time': fixations,
        'instruction_time_min': 2.0,
        'instruction_time_max': 2.0,
        'stim1_time': 1.0,
        'ISI': delays,
        'stim2_time': 1.0,
        'response_instruction_time': 1.0, 
        'response_time_max': 3.0,
        'text_holdout_time': 0.3,
        'ITI': 0.0,
        'instruction_time': np.full(n_trials, np.nan),
        'response_time': np.full(n_trials, np.nan),
        'slider_positions': [None] * n_trials,
        'trial_time': np.full(n_trials, np.nan),
        'resp_key': np.full(n_trials, np.nan),
        'complete_flag': 1,
    }
    
    # Get correct responses
    task_struct['correct_responses'] = get_correct_responses_training(task_struct)

    # Testing the photodiode (for even debug mode or Blackrock off)
    task_struct['photodiode_test_mode'] = True 

    # Setting up input devices
    # CEDRUS button box code commented out - using keyboard only
    # if task_struct['use_cedrus']:
    #     task_struct['handle'] = init_cedrus()
    #     task_struct['left_key'] = 4
    #     task_struct['right_key'] = 5
    #     task_struct['confirm_key'] = 3
    # else:
    task_struct['handle'] = None
    task_struct['left_key'] = 'left'  # Left arrow key
    task_struct['right_key'] = 'right'  # Right arrow key
    task_struct['confirm_key'] = 'space' # Space to submit
    task_struct['up_key'] = 'up'  # Up arrow key
    task_struct['down_key'] = 'down'  # Down arrow key
    
    task_struct['escape_key'] = 'q'
    task_struct['pause_key'] = 'p'
    task_struct['continue_key'] = 'c'
    
    # Creating display struct (same as main task)
    disp_struct = {}
    
    if debug:
        screen_size = [800, 600]
        full_screen = False
    else:
        screen_size = None
        full_screen = True
    
    gray = [0.31, 0.31, 0.31]
    
    # Opening window
    if screen_size is None:
        win = visual.Window(
            fullscr=full_screen,
            screen=0,
            color=gray,
            units='pix',
            allowGUI=not full_screen
        )
    else:
        win = visual.Window(
            size=screen_size,
            fullscr=full_screen,
            screen=0,
            color=gray,
            units='pix',
            allowGUI=not full_screen
        )
    
    # Use window-centered coordinates (origin at 0,0) so stimuli are centered
    center_x = 0
    center_y = 0
    width = win.size[0]
    height = win.size[1]

    dx = width / 5
    dy = height / 5

    stim_size = 250
    rew_width = 466
    rew_height = 350
    ph = stim_size
    pw = stim_size
    rw = rew_width
    rh = rew_height

    vertical_rects = [
        [-pw/2, dy - ph/2, pw/2, dy + ph/2],    # top
        [-pw/2, -dy - ph/2, pw/2, -dy + ph/2]   # bottom
    ]

    horizontal_rects = [
        [-dx - pw/2, -ph/2, -dx + pw/2, ph/2],  # left
        [dx - pw/2, -ph/2, dx + pw/2, ph/2],     # right
        [-rw/2, -rh/2, rw/2, rh/2]               # center
    ]

    reward_source_rect = [-width/2 + 160, -height/2 + 0, -width/2 + 1120, -height/2 + 720]
    
    # photodiode square
    box_size = height * 0.04
    offset = height * 0.02  # inset margin
    # Bottom-left corner position
    box_x = -width/2 + offset + box_size/2
    box_y = -height/2 + offset + box_size/2

    disp_struct['win'] = win
    disp_struct['screen_number'] = 0
    disp_struct['center_x'] = center_x
    disp_struct['center_y'] = center_y
    disp_struct['width'] = width
    disp_struct['height'] = height
    disp_struct['stim_size'] = stim_size
    disp_struct['rew_width'] = rew_width
    disp_struct['rew_height'] = rew_height
    disp_struct['reward_rect'] = horizontal_rects[2]
    disp_struct['reward_source_rect'] = reward_source_rect
    disp_struct['vertical_rects'] = vertical_rects
    disp_struct['horizontal_rects'] = horizontal_rects
    disp_struct['photodiode_box'] = [box_x, box_y, box_size, box_size]
    disp_struct['photodiode_dur'] = 0.05  # seconds

    image_cache = {}
    for trial_paths in task_struct['trial_stims']:
        for stim_path in trial_paths:  # [stim1_path, stim2_path]
            if stim_path not in image_cache:
                image_cache[stim_path] = visual.ImageStim(
                    win,
                    image=stim_path,
                    units="pix"
                    # don't set size/pos here, we'll set those per trial
                )

    # store in task_struct or local var
    disp_struct['image_cache'] = image_cache
    
    return task_struct, disp_struct

