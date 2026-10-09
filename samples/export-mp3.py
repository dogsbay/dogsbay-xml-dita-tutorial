#!/usr/bin/env python3
"""Export the open Audacity project as MP3 through mod-script-pipe."""
import os
import sys

if sys.platform == "win32":
    TO_PIPE = "\\\\.\\pipe\\ToSrvPipe"
    FROM_PIPE = "\\\\.\\pipe\\FromSrvPipe"
    EOL = "\r\n\0"
else:
    TO_PIPE = f"/tmp/audacity_script_pipe.to.{os.getuid()}"
    FROM_PIPE = f"/tmp/audacity_script_pipe.from.{os.getuid()}"
    EOL = "\n"


def send(to_pipe, from_pipe, command: str) -> str:
    """Send one command and return the reply, which ends with an empty line."""
    to_pipe.write(command + EOL)
    to_pipe.flush()
    reply = ""
    while True:
        line = from_pipe.readline()
        if line == "" or (line == "\n" and reply):
            return reply
        reply += line


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "episode.mp3"
    with open(TO_PIPE, "w") as to_pipe, open(FROM_PIPE) as from_pipe:
        for command in ("SelectAll:", "Normalize: PeakLevel=-1",
                        f"Export2: Filename={target} NumChannels=1"):
            print(send(to_pipe, from_pipe, command).strip())
