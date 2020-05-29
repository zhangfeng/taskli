import cmd
from subprocess import run, Popen, PIPE
import re
import filters

class Taskli(cmd.Cmd):

    base_prompt = 'Taskli ({})> '
    context_re = re.compile(r"Context '(\w+)' with filter '([^']*)' is currently applied\.\s*")
    update_context_re = re.compile(r".*Context (?:'(\w+)' |un)set\..*")
    context = ''
    filter = ''
    in_filters = []
    out_filters = []

    def default(self, line):
        run('clear')
        print('{', line, '}')
        for lin in Popen(['task'] + line.split(),
                          stdout=PIPE, text=True).stdout:
            self.scan_context(lin)
            print(self.post_filters(lin), end='', flush=True)

    def scan_context(self, lines):
        m = self.update_context_re.match(lines)
        if m:
            self.update_context(m[1])

    def update_prompt(self):
        if self.context != '_':
            self.prompt = self.base_prompt.format(self.context)
        else:
            self.prompt = self.base_prompt.format(self.filter)

    def update_context(self, context):
        if context is None:
            self.context = ''
        else:
            self.context = context
        self.update_prompt()

    def preloop(self):
        stdout_line = run(['task', 'context', 'show'],
                                      capture_output=True).stdout.decode()
        m = self.context_re.match(stdout_line)
        if m:
            self.context = m[1]
            self.filter = m[2]
        self.update_prompt()
        self.in_filters.append(filters.dot_cmd)

    def precmd(self, line):
        for flt in self.in_filters:
            line = flt(line)
        return line

    def post_filters(self, lines):
        for flt in self.out_filters:
            lines = flt(lines)
        return lines

    def do_EOF(self, arg):
        return True
