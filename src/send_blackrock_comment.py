
from src.cbmex_utils import (
        check_nsp_connections,
        get_next_log_entry,
        get_current_log_entry,
        gensave_filename,
        send_cbmex_comment,
    )

# Output folder
from pathlib import Path
output_folder = Path('..') / 'patientData' / 'neuralLogs'
output_folder.mkdir(parents=True, exist_ok=True)

LOG_PATH = None # to be set in main.py

def send_blackrock_comment(event: str, task: str, log_path: Path, additional_text: str = ""):
    """Send a comment to Blackrock NSP system via CBMEX.
    event: string like 'start', 'stim_on', 'finish', etc.
    task:  short task name: InstrWM
    log_path: path to the log CSV file
    additional_text: extra info to embed in the comment (e.g. 'trial=5; axis=2')
    """
    if not task or not event:
        # Mirror the "No comment provided" guard, but just raise in local code
        raise ValueError("Both 'event' and 'task' must be provided")

    check_nsp_connections()

    if event == "start":
        emu_num, subj_id, log_table = get_next_log_entry(log_path)
        file_string = gensave_filename(log_path, log_table, emu_num, subj_id, task)
    else:
        emu_num, subj_id, log_table = get_current_log_entry(log_path)
        file_string = gensave_filename(
            log_path,
            log_table,
            emu_num,
            subj_id,
            task,
            save_entry=False,
        )

    # This is the call that actually injects the comment into the NSP
    send_cbmex_comment(event, file_string, additional_text)
