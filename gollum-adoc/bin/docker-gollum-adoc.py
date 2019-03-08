#!/usr/bin/env python
"""
Docker launcher script.

Moved to python to make it more portable than the shell version (i.e. usable on
MacOS X)

The script accepts the following operations:

- start: starts a container in the background
- stop: stops the container if it is running
- status: shows if the container is running or not
- run: executes a command starting a container in the foreground
- exec: executes an interactive command in a running container

If the operation is 'run' the container is started using the command:

{{{
$ docker start -a -i COMMAND
}}}

The files GROUP_FILE, PASSWD_FILE and DOCKER_SUDOERS_FILE are generated by this
script to allow the host user to impersonate as user:user inside the docker
container, access to his or her home directory under /user and call sudo inside
the container without using passwords.
"""
# -------
# IMPORTS
# -------
from __future__ import print_function

import os
import sys
import tarfile
import tempfile
import time
from io import BytesIO
from subprocess import PIPE, Popen, check_output

# ---------
# VARIABLES
# ---------

# Default container name
CONTAINER_NAME = "gollum-adoc"

# Docker related variables
DOCKER_COMMAND = "docker"
DOCKER_IMAGE = "stodh/gollum-adoc"


# ---------
# FUNCTIONS
# ---------
def append_to_file_in_docker(container_id, fdir, fname, fdata):
    """
    Function to append to a file into a docker container using tarfiles.

    The function generates a memory based tarfile that contains a file with the
    given name, contents, mode and user and group ownership and expands the tar
    on the destination path.
    """
    # Read old data
    cmnd = [
        DOCKER_COMMAND, 'cp', '{}:{}/{}'.format(container_id, fdir, fname), '-'
    ]
    p1 = Popen(cmnd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    otmp = tempfile.SpooledTemporaryFile()
    otmp.write(p1.stdout.read())
    otmp.seek(0)
    otar = tarfile.open(fileobj=otmp)
    oinf = otar.getmember(fname)
    obuf = otar.extractfile(oinf)
    odat = obuf.read()
    otar.close()
    otmp.close()
    # Append new data & prepare new TarInfo
    if type(fdata) is bytes:
        bfdata = fdata
    else:
        bfdata = fdata.encode('utf-8')
    ndat = odat + bfdata
    ninf = oinf
    ninf.size = len(ndat)
    # Create new tarfile and write data
    cmnd = [DOCKER_COMMAND, 'cp', '-', '{}:{}'.format(container_id, fdir)]
    p2 = Popen(cmnd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    ntmp = tempfile.SpooledTemporaryFile()
    ntar = tarfile.TarFile(fileobj=ntmp, mode='w')
    nbytes = BytesIO(ndat)
    ntar.addfile(tarinfo=ninf, fileobj=nbytes)
    ntar.close()
    ntmp.seek(0)
    res = p2.communicate(input=ntmp.read())
    ntmp.close()
    return res


def write_file_to_docker(container_id,
                         fdir,
                         fname,
                         fdata,
                         fmode,
                         fuid=0,
                         fgid=0,
                         funame='root',
                         fgname='root'):
    """
    Function to write a file into a docker container using tarfiles.

    The function generates a memory based tarfile that contains a file with the
    given name, contents, mode and user and group ownership and expands the tar
    on the destination path.
    """
    # mode 420 == 0644
    info = tarfile.TarInfo(name=fname)
    info.mode = fmode
    info.mtime = time.time()
    info.uid = fuid
    info.gid = fgid
    info.uname = funame
    info.gname = fgname
    if type(fdata) is bytes:
        bfdata = fdata
    else:
        bfdata = fdata.encode('utf-8')
    info.size = len(bfdata)
    fbytes = BytesIO(bfdata)
    cmnd = [DOCKER_COMMAND, 'cp', '-', '{}:{}'.format(container_id, fdir)]
    p = Popen(cmnd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    tmp = tempfile.SpooledTemporaryFile()
    tar = tarfile.TarFile(fileobj=tmp, mode='w')
    tar.addfile(tarinfo=info, fileobj=fbytes)
    tar.close()
    tmp.seek(0)
    res = p.communicate(input=tmp.read())
    tmp.close()
    return res


# ----
# MAIN
# ----

# Process arguments
DEFAULT_OPERATION = 'attach'
if len(sys.argv) > 1:
    OPERATION = sys.argv[1]
else:
    OPERATION = DEFAULT_OPERATION
if OPERATION not in ('start', 'stop', 'status', 'attach', 'exec', 'run'):
    print("Usage: {} [start|stop|status|attach|exec|run]".format(sys.argv[0]))
    print("")
    print("If no operation is given the default one is '{}'".format(
        DEFAULT_OPERATION))
    sys.exit(0)
CONTAINER_COMMAND = []
if OPERATION in ('exec', 'run'):
    if len(sys.argv) > 2:
        CONTAINER_COMMAND = sys.argv[2:]
    else:
        print("The operation '{}' needs a command for the container".format(
            OPERATION))
        sys.exit(0)

# Get effective uid and gid
EUID = os.geteuid()
EGID = os.getegid()

# Compute work dir, docker data dir and docker file paths
WORK_DIR = os.getcwd()

# Docker container name
DOCKER_CONTAINER_NAME = CONTAINER_NAME

GET_CONTAINER_ID_COMMAND = [
    DOCKER_COMMAND,
    'ps',
    '--quiet',
    '--filter',
    'name={}'.format(DOCKER_CONTAINER_NAME),
]
CONTAINER_ID = check_output(
    GET_CONTAINER_ID_COMMAND, universal_newlines=True).split('\n')[0]

# Check operations
if OPERATION == 'status':
    if CONTAINER_ID == "":
        print("Container '{}' not running".format(DOCKER_CONTAINER_NAME))
    else:
        print("Container '{}' running with ID '{}'".format(
            DOCKER_CONTAINER_NAME, CONTAINER_ID))
    sys.exit(0)
elif OPERATION == 'stop':
    if CONTAINER_ID == "":
        print("Container '{}' not running".format(DOCKER_CONTAINER_NAME))
    else:
        print("Stopping container '{}' running with ID '{}'".format(
            DOCKER_CONTAINER_NAME, CONTAINER_ID))
        STOP_DOCKER_COMMAND = [
            DOCKER_COMMAND,
            'stop',
            CONTAINER_ID,
        ]
        STOP_OUTPUT = check_output(
            STOP_DOCKER_COMMAND, universal_newlines=True).split('\n')[0]
        if STOP_OUTPUT != CONTAINER_ID:
            print("Error stoping the container: {}".format(STOP_OUTPUT))
            sys.exit(1)
    sys.exit(0)

# If we are here the OPERATION is one of 'start', 'exec' or 'run'; in all cases
# we have to create the container if it is not running
if CONTAINER_ID != "":
    if OPERATION == 'start':
        print("Container '{}' already running with ID '{}'".format(
            DOCKER_CONTAINER_NAME, CONTAINER_ID))
        sys.exit(0)
else:
    # Create docker command
    CREATE_DOCKER_COMMAND = [
        DOCKER_COMMAND,
        'create',
        '--tty',
        '--interactive',
        '--name={}'.format(DOCKER_CONTAINER_NAME),
        '--rm=true',
        '--env=LANG',
        '--publish=4000:4000',
        '--user={}:{}'.format(EUID, EGID),
        '--volume={}:/documents'.format(WORK_DIR),
        '--volume={}:/user'.format(os.path.expanduser('~')),
    ]
    CREATE_DOCKER_COMMAND.append(DOCKER_IMAGE)
    # Pass command line args if we are using the 'run' operation
    if OPERATION == 'run':
        CREATE_DOCKER_COMMAND.extend(CONTAINER_COMMAND)
    # Create container
    CONTAINER_ID = check_output(
        CREATE_DOCKER_COMMAND, universal_newlines=True).split('\n')[0]
    # Create files inside the container if needed
    if EGID != 0:
        # group file
        fdir = "/etc"
        fname = 'group'
        fdata = "user:x:{}:\n".format(EGID)
        append_to_file_in_docker(CONTAINER_ID, fdir, fname, fdata)
    if EUID != 0:
        # passwd file
        fdir = "/etc"
        fname = 'passwd'
        fdata = "user:x:{}:{}:Docker user:/user:/bin/bash\n".format(EUID, EGID)
        append_to_file_in_docker(CONTAINER_ID, fdir, fname, fdata)
        # sudoers file
        fdir = "/etc/sudoers.d"
        fname = "docker-user"
        fdata = "#{} ALL=(ALL) NOPASSWD: ALL\n".format(EUID)
        fmode = 288  # 288 == 0440
        write_file_to_docker(CONTAINER_ID, fdir, fname, fdata, fmode)
    # Start container
    if OPERATION == 'run':
        RUN_DOCKER_COMMAND = [
            DOCKER_COMMAND, 'start', '--interactive', '--attach', CONTAINER_ID
        ]
        os.execvp(DOCKER_COMMAND, RUN_DOCKER_COMMAND)
    else:
        START_DOCKER_COMMAND = [DOCKER_COMMAND, 'start', CONTAINER_ID]
        START_OUTPUT = check_output(
            START_DOCKER_COMMAND, universal_newlines=True).split('\n')[0]
        print(START_OUTPUT)

# Process commands
if OPERATION == 'start':
    print("Container '{}' started with ID '{}'".format(DOCKER_CONTAINER_NAME,
                                                       CONTAINER_ID))
    sys.exit(0)
elif OPERATION == 'attach':
    ATTACH_DOCKER_COMMAND = [DOCKER_COMMAND, 'attach', CONTAINER_ID]
    os.execvp(DOCKER_COMMAND, ATTACH_DOCKER_COMMAND)
elif OPERATION == 'exec':
    EXEC_DOCKER_COMMAND = [
        DOCKER_COMMAND, 'exec', '--interactive', '--tty', CONTAINER_ID
    ]
    EXEC_DOCKER_COMMAND.extend(CONTAINER_COMMAND)
    os.execvp(DOCKER_COMMAND, EXEC_DOCKER_COMMAND)
elif OPERATION == 'run':
    print("Container '{}' is running with ID '{}'".format(
        DOCKER_CONTAINER_NAME, CONTAINER_ID))
    print("Stop it and call 'run' again or use 'attach' and invoke the command"
          " interactively")
    sys.exit(1)