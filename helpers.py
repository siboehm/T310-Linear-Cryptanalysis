# Thanks: https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py
# Author : Om "Ethcelon" Bhallamudi
# Version : 1.b1
import argparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ArgParseError(Exception):
     def __init__(self, value):
         self.value = 'Argument error\n' + value
     def __str__(self):
         return repr(self.value)

def ret_str(*args):
    "Returns string of args separated by an underscore."
    try:
        return '_'.join(map(lambda x: str(x), args))
    except Exception as e:
        raise e

# Om says: my AWESOME comment printer/LOGGER. nyae?
def comment(*args, **kwargs):
    "Prints args & kwgars to stdout, uses a delimiter ( typically // )."
    log = True

    delimiter = '//'
    if log:
        with open('log.txt', 'a') as w:
            for arg in args:
                w.write('{delimiter} {com}\n'.format(com=arg, delimiter=delimiter))
            for key, value in kwargs.iteritems():
                w.write('{delimiter} {key} = {value}\n'.format(key=key, value=value, delimiter=delimiter))
    else:
        for arg in args:
            print '{delimiter} {com}'.format(com=arg, delimiter=delimiter)
        for key, value in kwargs.iteritems():
            print '{delimiter} {key} = {value}'.format(key=key, value=value, delimiter=delimiter)

def pp_eqn(ls):
    "Prints lhs=rhs type equations. Look at the code to configure."
    if type(ls) is not list:
        ls = [ls]

    for x in ls:
        try:
            lhs, rhs = x.split('=')
            s = ''
            s += bcolors.OKBLUE + lhs + bcolors.ENDC
            s += '=' + bcolors.OKGREEN
            rhs = rhs.replace('*', bcolors.OKBLUE +  '*' + bcolors.OKGREEN)
            rhs = rhs.replace('+', bcolors.OKBLUE +  '+' + bcolors.OKGREEN)
            s += rhs + bcolors.ENDC
            print s

        except Exception as e:
            print x

def pp_args(args):
    comment('======ARGS======')
    for key, value in args.iteritems():
        comment('{} = {}'.format(key, value))
    comment('='*16)

def pretty_print(str):
    try:
        s = str.split(' ')
        ss = ''
        if s[0] == 'W':
            ss += bcolors.OKBLUE + 'W' + bcolors.ENDC
        elif s[0] == 'C':
            ss += bcolors.OKGREEN + 'C' + bcolors.ENDC
        elif s[0] == 'I':
            ss += bcolors.OKGREEN + 'I' + bcolors.ENDC
        elif s[0] == 'O':
            ss += bcolors.FAIL + 'O' + bcolors.ENDC
        elif s[0] == '+':
            ss += bcolors.FAIL + '+' + bcolors.ENDC
        print ss + ' ' + ' '.join(s[1:])

    except Exception as e:
        print str

def parse_args(args):
    """
        abc.exe Nr /ins8
        abc.exe 40..80 /ins8 /fix200
        /insXX XX=1,8 or more
        sequence of runs and store results in T310_Timings.txt
        41,15.71s,command line\n 42,23.05s
        encryption step if Nr >=127*13
        # /fix50 - both parts, random subset of 230 bits
        > random IVs by default (DONE)
        > /cIV /xl0 /sat /cryptominisat64291
        "if exist ax64.exe ax64.exe 4000 Simon_6R_fixk0_block64_key128_2CP.txt"
        "if exist ax64.exe ax64.exe 4444 /cryptominisat64291
        Simon_6R_fixk0_block64_key128_2CP.txt"
    """

    """
    if len(args) < 2:
        raise ArgParseError("Need number of rounds\n Usage: \n 1. prog_name Nr \n 2. progname Nr..Nr \n   Nr: int")
    from config import default_args

    parsed = default_args

    parsed['prog_name'] = args[0]
    num_rounds = args[1]
    """
    ### Killians notes
    ## At the end of this block:
    ## num_rounds should be filled
    ## Parse ins, parse sat, parse fix and parse key

    parser = argparse.ArgumentParser()
    parser.add_argument("--num_rounds", metavar='N', type=int)
    parser.add_argument("--high_rounds", type=int, nargs='?')
    parser.add_argument("--sat", help="Sat: is sat set", action="store_true")
    parser.add_argument("--bits-fixed", help="Set how many bits are fixed", type=int)
    parser.add_argument("--instances", help="How many instances", nargs='+', type=int)
    parser.add_argument("--xl", help="How many", action="store_true")
    parser.add_argument("--key", help="the key")
    parser.add_argument("--cryptominisat", help="How manances",action="store_true")
    parser.add_argument("--civ", help="How many instances", type=int)
    parser.add_argument("--t310set", help="", type=int)
    parsed_args = parser.parse_args()
    parsed = {}
    parsed['rounds'] = parsed_args.num_rounds
    if parsed_args.high_rounds:
        high_rounds = parsed_args.high_rounds
        ## Need check for :: Usage: NrX-NrY where NrX < NrY and +ve"
    parsed['sat'] = parsed_args.sat
    parsed['fix'] = parsed_args.bits_fixed
    parsed['ins'] = parsed_args.instances
    parsed['xl'] = parsed_args.xl
    
    to_parse = []
    if 'key' in to_parse:
        arg = to_parse['key']
        try:
            knum = int(arg)
            parsed['key'] = int(arg)
        except Exception as e:
            parsed['key'] = 26
    else:
        parsed['key'] = 26

    if 'old' in to_parse:
        arg = to_parse['old']

        if arg == '937':
            parsed['old'] = 'works_0937'
        else:
            parsed['old'] = 'ax64'

    else:
        parsed['old'] = 'ax64'

    return parsed

def get_command(filename, run, actions):
    from codegen import keynum

    f = [filename, str(run['rounds'])]
    f.append('/ins%d' % run['ins'])
    f.append('/fix%d' % run['fix'])
    if actions['sat']:
        f.append('/sat')
    if actions['xl']:
        f.append('/xl')
    f.append('/T310set%d' % keynum)
    return ' '.join(f)

def get_filename(run, actions):
    from codegen import keynum

    f = ['ARGON', str(run['rounds']) + 'R', ]
    f.append('INS%d' % run['ins'])
    f.append('FIX%d' % run['fix'])
    if actions['sat']:
        f.append('SAT')
    if actions['xl']:
        f.append('XL')
    f.append('LZS%d' % keynum)
    return '_'.join(f)

def genruns(parsed_args):
    runs = [] # This is a queue

    actions = {
        'xl' : parsed_args['xl'],
        'sat' : parsed_args['sat']
    }

    rounds = parsed_args['rounds']

    if type(rounds) is int:
        runs.append({'rounds': rounds})
    else:
        for y in xrange(rounds[0], rounds[1]+1):
            runs.append({'rounds' : y})

    ins = parsed_args['ins']
    temp = []

    for x in runs:
        for y in ins:
            temp.append({
                'rounds' : x['rounds'],
                'ins' : y,
            })
    runs = temp
    temp = []
    fix = parsed_args['fix']

    if type(fix) is int:
        for x in runs:
            x['fix'] = fix

    else:
        for x in runs:
            for y in fix:
                temp.append({
                    'rounds' : x['rounds'],
                    'ins' : x['ins'],
                    'fix' : y,
                })

        runs = temp

    passalong = None #parsed_args['unknowns']

    return runs, actions, passalong

def write_runs_to_file(runs, actions, passalong, filename='runs.txt'):
    f = open(filename, 'w')

    f.write('// RUN\n')
    f.write('// xl = {}\n'.format(actions['xl']))
    f.write('// sat = {}\n'.format(actions['sat']))
    f.write('// PASS ALONGS = {}\n'.format(passalong))
    f.write('// TOTAL RUNS = {}\n'.format(len(runs)))

    for x in runs:
        f.write( 'rounds={}, ins={}, fix={}\n'.format(x['rounds'], x['ins'], x['fix']))

    f.close()

def timed_process(proc):
    from  sys import platform

    import subprocess
    import time

    start_time = time.time()
    process = subprocess.Popen(proc.split(' '), shell=True)
    pretty_print('O AX64 says:')
    comment('O AX64 says:')

    try:
        process.wait()
        #while True:
        #    line = process.stdout.readline()
        #    if line != '':
        #        pretty_print('+ '+line.rstrip())
        #        comment('+ '+line.rstrip())
        #
        #    else:
        #        break

    except subprocess.CalledProcessError as e:
        pretty_print ('O {} returned with (code {}): {}'.format(e.cmd, e.returncode, e.output))

    except Exception as e:
        raise e # bigly bad

    elapsed = time.time() - start_time
    pretty_print('O ax64 returned in {}'.format(elapsed))
    comment('O ax64 returned in {}'.format(elapsed))

    return elapsed

def write_csv(filename, TITLE, items):
    import os.path
    strings = []
    exists = os.path.isfile(filename)
    mode = 'a'

    if not exists:
        strings.append(TITLE+'\n')
        mode = 'w'
    for item in items:
        strings.append(','.join([str(x) for x in item])+'\n')

    with open(filename, mode) as w:
        w.writelines(strings)
        w.close()

    return

def bin2hex_str(R):
    return format(int(R, 2), 'x').upper()

def bin2hex_str16(R):
    return format(int(R, 2), '0>16x').upper()

def bin2hex_str60(R):
    return format(int(R, 2), '0>60x').upper()

def bin2hex_str9(R):
    return format(int(R, 2), '0>9x').upper()

if __name__ == '__main__':
    import sys

    try:
        #parse_args(sys.argv)
        timed_process('/bin/ls -altr')
    except ArgParseError as e:
        print e.value
    except Exception as e:
        print "unknown error:\n", e
