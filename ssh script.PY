import subprocess
DEFAULT_TIMEOUT_IN_SECONDS= 1800
def execute_remote_command(command, server_name, ssh_user, timeout_in_seconds=DEFAULT_TIMEOUT_IN_SECONDS):
    command = 'ssh -qo Batchmode=yes {ssh_user}@{server_name} '{command}'".format(**locals())
    retrun execute_command(command, timeout_in_seconds=DEFAULT_TIMEOUT_IN_SECONDS)
    
def execute_command(command, timeout_in_seconds=DEFAULT_TIMEOUT_IN_SECONDS):
    import shlex
    arguments = shelx.split(command)
    process = supprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        stdout, stderr = process.communicate(timeout=timeout_in_seconds)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
    return abs(process.returncode), stdout.decode(encoding=UTF8), stderr.decode(encoding=UTF8)
            
