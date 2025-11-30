"""
Lookup table to determine instruction prompt used in each trial.
"""

def get_instruction_text(category, trial_axis_name, prompt_variant):
    """
    Get instruction text based on trial parameters.
    
    Parameters:
    -----------
    category : int
        Category index (0=Animals, 1=Cars, 2=Faces, 3=Fruits)
    trial_axis_name : str
        Name of the axis ('New', 'Geometry', 'Count', 'Colorful')
    prompt_variant : bool or int
        Which prompt variant to use
    
    Returns:
    --------
    text : str
        Instruction text for the trial
    """
    # Convert to boolean for easier handling
    prompt_variant = bool(prompt_variant)

    if trial_axis_name == 'New':
        if prompt_variant: # younger/newer
            if category == 2: # faces
                text = f'Choose image with the younger item(s)'
            else: # cars
                text = f'Choose image with the newer item(s)'
        else: # older/less modern
            if category == 2: 
                text = f'Choose image with the older item(s)'
            else:
                text = f'Choose image with the older item(s)'
    
    elif trial_axis_name == 'Geometry':
        if prompt_variant:
            text = f'Choose image with the more rounded item(s)'
        else:
            text = f'Choose image with the more elongated item(s)'
    
    elif trial_axis_name == 'Count':
        if prompt_variant:
            text = f'Choose image with more items'
        else:
            text = f'Choose image with fewer items'
    
    elif trial_axis_name == 'Colorful':
        if prompt_variant:
            text = f'Choose image with the more colorful item(s)'
        else:
            text = f'Choose image with the less colorful item(s)'
    
    else:
        text = ''
    
    return text
