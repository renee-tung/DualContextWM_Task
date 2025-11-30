from os import path, listdir, getenv
from pandas import read_csv
from subprocess import run
from cerebus import cbpy

PORT_NAMES = ['NSP1', 'NSP2']

def check_nsp_connections():    
    ips = []
    ips = [getenv("NSP1_IP"), getenv("NSP2_IP")]
    if not all(ips):
        raise RuntimeError("Missing NSP1_IP / NSP2_IP environment variables.")
   
    for inst, address in enumerate(ips):   # list the IP addresses as 0: address1, 1: address2 etc.
        try:
            cbpy.open(instance=inst, parameter={'inst-addr':address})   # Use cpby to create a link per address, treating the nsp as a central machine
        except:
            print(f"Issue opening NSP{inst+1}")
            raise ConnectionError("Error connecting to one or more NSPs")
    return ips

def get_next_log_entry(log_path):
    # get next entry info from log
    log_table = read_csv(log_path)
    try:
        emu_num = log_table['emu_id'][log_table.shape[0]-1] + 1
    except KeyError as e:
        print(e)
        emu_num = 1
    subj_id = path.basename(log_path).split('_')[0].split('.')[0]
    return emu_num, subj_id, log_table

def get_current_log_entry(log_path):
    log_table = read_csv(log_path)
    try:
        emu_num = log_table['emu_id'][log_table.shape[0]-1]
    except KeyError as e:
        print(e)
        raise KeyError("Log table is empty!")
    subj_id = path.basename(log_path).split('_')[0].split('.')[0]
    return emu_num, subj_id, log_table
    
def gensave_filename(log_path, log_table, emu_num, subj_id, task, save_entry=True):
    # generate filename string
    file_string = f'EMU-{emu_num:04}_subj-{subj_id}_{task}'
    
    # Save the new task entry in the log file if save_entry true
    if save_entry:
        log_table.loc[len(log_table)] = [emu_num, file_string]
        log_table.to_csv(log_path, index=False)

    # return file string for comments sake
    return file_string

def send_cbmex_comment(event, file_string, additional_text='', **kwargs):
    # Instantiate the event message and color
    eventCode = ''
    eventColor = (0,255,255,255)#16777215
    closeAfter = False

    # Adjust behavior on event
    match event:
        #tbgr
        case 'start':  # On start, send a green start message
            eventCode = f'$TASKSTART {file_string}'
            eventColor = (0,0,255,0)#65280
        case 'stop':   # On stop, send a pink stop message
            eventCode = f'$TASKSTOP {file_string}'
            eventColor =  (0,255,0,255)#16711935
            closeAfter = True
        case 'kill':  # On kill, send a red kill message
            eventCode = f'$TASKKILL {file_string}'
            eventColor = (0,0,0,255)#255
            closeAfter = True
        case 'error': # On error, send a red error message
            eventCode = f'$TASKERR {file_string}'
            eventColor = (0,0,0,255)#255
            closeAfter = True
        case 'annotate': # On annotate, send a blue generic event message
            eventCode = additional_text
            eventColor = (0,255,0,0)#16711680
        case _:          # In any other case, send a white message with the event name as the message
            eventCode = f'{event}-{file_string}'

    for idx, _ in enumerate(PORT_NAMES):
        # combine event code with nsp suffix to sen d as comment
        comment = f'{eventCode}_NSP-{idx+1}'
        
        # Send the comment to blackrock
        cbpy.set_comment(comment, rgba_tuple=eventColor, instance=idx)

    
    # On stop, kill or error, close the link to the NSP
    if closeAfter:
        cbpy.close(0) # NSP-1
        cbpy.close(1) # NSP-2
       


