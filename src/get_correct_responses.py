"""
Given the trial conditions and prompts, get the expected correct response
for each trial in advance (to compare with actual button presses later).
"""

import numpy as np
from pathlib import Path

def get_correct_responses(task_struct):
    """
    Calculate correct responses for all trials.
    
    Parameters:
    -----------
    task_struct : dict
        Task structure containing trial information
    
    Returns:
    --------
    correct_responses : numpy array
        Array of correct response keys (1 or 2) for each trial
    """
    # Getting unique characteristics of each stimulus
    # Note: Paths need to be adjusted based on actual stimulus folder structure

    stim_folder = 'stimuli/Task_Stim_New_v1/'

    stims = [
        [stim_folder + 'Animals/Pair1/flamingo_17s.jpg', ['Colorful', 'Multiple']],
        [stim_folder + 'Animals/Pair1/groundhog_09s.jpg', ['notColorful', 'Single']],
        [stim_folder + 'Animals/Pair2/otter_05s.jpg', ['notColorful', 'Single']],
        [stim_folder + 'Animals/Pair2/parrot_05s.jpg', ['Colorful', 'Multiple']],
        [stim_folder + 'Animals/Pair3/alpaca_04s.jpg', ['notColorful', 'Multiple']],
        [stim_folder + 'Animals/Pair3/bug_06s.jpg', ['Colorful', 'Single']],
        [stim_folder + 'Cars/Pair1/bus_01b.jpg', ['notColorful', 'Old']],
        [stim_folder + 'Cars/Pair1/bus_07n.jpg', ['Colorful', 'New']],
        [stim_folder + 'Cars/Pair2/car_04s.jpg', ['Colorful', 'New']],
        [stim_folder + 'Cars/Pair2/van_10s.jpg', ['notColorful', 'Old']],
        [stim_folder + 'Cars/Pair3/car_09s.jpg', ['notColorful', 'New']],
        [stim_folder + 'Cars/Pair3/jeep_09s.jpg', ['Colorful', 'Old']],
        [stim_folder + 'Faces/Pair1/boy_04s.jpg', ['New', 'Elongated']],
        [stim_folder + 'Faces/Pair1/man_10s.jpg', ['Old', 'Round']],
        [stim_folder + 'Faces/Pair2/girl_01b.jpg', ['New', 'Round']],
        [stim_folder + 'Faces/Pair2/woman_02s.jpg', ['Old', 'Elongated']],
        [stim_folder + 'Faces/Pair3/man_06s.jpg', ['Old', 'Elongated']],
        [stim_folder + 'Faces/Pair3/man_08s.jpg', ['New', 'Round']],
        [stim_folder + 'Fruits/Pair1/apple_12s.jpg', ['Single', 'Round']],
        [stim_folder + 'Fruits/Pair1/carrot_03s.jpg', ['Multiple', 'Elongated']],
        [stim_folder + 'Fruits/Pair2/blueberry_10s.jpg', ['Multiple', 'Round']],
        [stim_folder + 'Fruits/Pair2/mulberry_11s.jpg', ['Single','Elongated']],
        [stim_folder + 'Fruits/Pair3/banana_07s.jpg', ['Single', 'Elongated']],
        [stim_folder + 'Fruits/Pair3/peach_10n.jpg', ['Multiple', 'Round']],
    ]
    
    n_trials = task_struct['n_trials']
    correct_responses = np.full(n_trials, np.nan)
    # trial_variant = np.array(task_struct['anti_task']) + np.array(task_struct['prompt_variant'])
    trial_variant = np.array(task_struct['prompt_variants'])
    
    for t_i in range(n_trials):
        axis = task_struct['trial_axis'][t_i]
        category = task_struct['trial_categories'][t_i]
        trial_axis_name = task_struct['category_and_axis'][1][category][axis]
        
        # Determine target feature based on trial axis and variant
        if trial_axis_name == 'Colorful':
            target_feature = 'notColorful'
            if trial_variant[t_i] == 1:
                target_feature = 'Colorful'
        elif trial_axis_name == 'Count':
            target_feature = 'Single'
            if trial_variant[t_i] == 1:
                target_feature = 'Multiple'
        elif trial_axis_name == 'Geometry':
            target_feature = 'Elongated'
            if trial_variant[t_i] == 1:
                target_feature = 'Round'
        elif trial_axis_name == 'New':
            target_feature = 'Old'
            if trial_variant[t_i] == 1:
                target_feature = 'New'
        else:
            target_feature = ''
        
        trial_text = [task_struct['left_text'][t_i], task_struct['right_text'][t_i]]
        
        # Other conditions than identical
        stim1_path = task_struct['trial_stims'][t_i][0]
        stim2_path = task_struct['trial_stims'][t_i][1]
        
        # Find stimulus indices
        stim1_idx = None
        stim2_idx = None
        for i, (stim_path, _) in enumerate(stims):
            if stim_path in stim1_path or Path(stim1_path).name in stim_path:
                stim1_idx = i
            if stim_path in stim2_path or Path(stim2_path).name in stim_path:
                stim2_idx = i
        
        if stim1_idx is None or stim2_idx is None:
            continue
        
        stim_features = [stims[stim1_idx][1], stims[stim2_idx][1]]
        # Check which stimulus has the target feature (1 = first, 2 = second)
        stim_with_target_feature = 2 if target_feature in stim_features[1] else 1
        
        if stim_with_target_feature == 1:
            correct_key = [i for i, text in enumerate(trial_text, 1) if 'First' in text][0]
        else:
            correct_key = [i for i, text in enumerate(trial_text, 1) if 'Second' in text][0]
        
        correct_responses[t_i] = correct_key
    
    return correct_responses

