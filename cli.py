import cmd
import subprocess

class Taskli(cmd.Cmd):

    prompt = 'Taskli ()> '

    def default(self, line):
        subprocess.run(['task'] + line.split())

    def do_EOF(self, arg):
        return True
