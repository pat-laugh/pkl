#!/usr/bin/env python3

import os

join = os.path.join

dir_xkb = '/usr/share/X11/xkb/'
dir_data = 'data'
dir_matches = join(dir_data, 'matches')
dir_input = join(dir_data, 'xkb')

DIR_TEMP = '.install_files'

def process_file(d_name, f_name):
    matches_path = join(dir_matches, d_name, f_name)
    xkb_path = join(dir_xkb, d_name, f_name)
    with open(matches_path) as f:
        matches = f.read().splitlines()
    with open(xkb_path) as f:
        lines_xkb = f.read().splitlines()
    if len(matches) == 0:
        i_xkb = 1
    else:
        curr_match = 0
        for i, line in enumerate(lines_xkb):
            if curr_match == len(matches):
                break
            if line.find(matches[curr_match]) >= 0:
                curr_match += 1
                i_xkb = i + 1
        else:
            raise Exception('')
    temp_file = join(DIR_TEMP, '%s_%s' % (d_name, f_name))
    input_file = join(dir_input, d_name, f_name)
    with open(input_file) as f:
        num_lines_input = len(f.read().splitlines())
    return [
        ' '.join([
            'cat',
            '<(head -n %i %s)' % (i_xkb, xkb_path),
            '<(tail -n +%i %s)' % (i_xkb + num_lines_input, xkb_path),
            '>%s' % (temp_file),
        ]),
        'sudo cp %s %s' % (temp_file, xkb_path),
    ]

def install_script_lines():
    install_lines = [
        '#!/usr/bin/env bash',
        '', 'mkdir -p ' + DIR_TEMP,
    ]
    for d_name in os.listdir(dir_matches):
        dir_path = join(dir_matches, d_name)
        for f_name in os.listdir(dir_path):
            install_lines += [''] + process_file(d_name, f_name)
    return install_lines + [
        '', 'rm -r ' + DIR_TEMP,
        '', 'echo Log out and log back in to complete the installation',
    ]

if __name__ == '__main__':
    print('\n'.join(install_script_lines()))
