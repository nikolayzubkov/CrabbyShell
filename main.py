import os
import subprocess
from rich import print

# ⟩ ⎩⎭
def execute_command(command):
    try:
        if "|" in command:
            # save for restoring later on
            s_in, s_out = (0, 0)
            s_in = os.dup(0)
            s_out = os.dup(1)

            # first command takes commandut from stdin
            fdin = os.dup(s_in)

            # iterate over all the commands that are piped
            for cmd in command.split("|"):
                # fdin will be stdin if it's the first iteration
                # and the readable end of the pipe if not.
                os.dup2(fdin, 0)
                os.close(fdin)
                # restore stdout if this is the last command
                if cmd == command.split("|")[-1]:
                    fdout = os.dup(s_out)
                else:
                    fdin, fdout = os.pipe()

                # redirect stdout to pipe
                os.dup2(fdout, 1)
                os.close(fdout)

                try:
                    subprocess.run(cmd.strip().split())
                except Exception:
                    print("[red]🦀 Crabby can't find the command: [red] \"[cyan]{}[cyan]\"".format(cmd.strip()))

            # restore stdout and stdin
            os.dup2(s_in, 0)
            os.dup2(s_out, 1)
            os.close(s_in)
            os.close(s_out)
        else:
            subprocess.run(command.split(" "))
    except Exception:
        print("[red]🦀 Crabby cant find the command: [red] \"[cyan]{}[cyan]\"".format(command))

def psh_cd(path):
    """convert to absolute path and change directory"""
    try:
        os.chdir(os.path.abspath(path))
    except Exception:
        print("[red]🦀 Crabby can't find the directory: [red] \"[cyan]{}[cyan]\"".format(path))


def psh_help():
    print("""[cyan]Crab shell: A shell for rustaceans 🦀 [cyan]""")


def main():
    while True:
       	#inp = Prompt.ask("[cyan]⎩{}⎭[cyan] [green]⟩[green] ".format(os.getcwd()), show_choices=False)
        #inp = PromptBase.get_input("[cyan]⎩{}⎭[cyan] [green]⟩[green] ".format(os.getcwd()))
        print(f"[cyan]⎩{os.getcwd()}⎭[cyan] [green]⟩[green] ", end="")
        inp = input()
        if inp == "exit":
            break
        elif inp == "cd":
            psh_cd(home)
        elif inp[:3] == "cd ":
            psh_cd(inp[3:])
        elif inp == "help":
            psh_help()
        else:
            execute_command(inp)


if '__main__' == __name__:
    main()
