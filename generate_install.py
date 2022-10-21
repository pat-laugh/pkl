#!/usr/bin/env python3

import os

dir_xkb = '/usr/share/X11/xkb/'
dir_data = 'data'
dir_matches = os.path.join(dir_data, 'matches')
dir_input = os.path.join(dir_data, 'xkb')

def install_script_lines():
    install_lines = ['#!/usr/bin/env bash']
    for d_name in os.listdir(dir_matches):
        dir_path = os.path.join(dir_matches, d_name)
        for f_name in os.listdir(dir_path):
            f_path = os.path.join(dir_path, f_name)
            xkb_path = os.path.join(dir_xkb, d_name, f_name)
            with open(f_path) as f:
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
                    assert(False)
            install_lines.append('')
            install_lines.append('mkdir -p %s' % (os.path.join('backup', d_name)))
            install_lines.append(' '.join(['cp', xkb_path,
                os.path.join('backup', d_name, f_name)]))
            install_lines.append(' '.join([
                'sudo',
                'cat',
                '<(head -n %i %s)' % (i_xkb, xkb_path),
                '<(cat %s)' % (os.path.join(dir_input, d_name, f_name)),
                '<(tail -n -%i %s)' % (i_xkb, xkb_path),
                '>%s' % (xkb_path),
            ]))
    install_lines.append('')
    install_lines.append('echo Log out and log back in to complete the installation')
    return install_lines

if __name__ == '__main__':
    print('\n'.join(install_script_lines()))
