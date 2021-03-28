#! /usr/bin/env python3

import subprocess


def ip_rtt(host):
    command = f"asterisk -rx 'pjsip show aor {host.split('/')[0]}'"
    ips = subprocess.Popen([command], shell=True,
                           stdout=subporcess.PIPE, encoding='utf-8')
    ips = list(ips.communicate())
    ip = ''
    rtt = ''
    for line in ips[0].split('\n'):
        if '/sip:' in line and '@' in line:
            ip = line.split('/sip:')[1].split()[0].split(':')[0].split('@')[1]
            rtt = line.split('/sip:')[1].split()[-1]
        elif '/sip' in line and '@' not in line:
            ip = line.split('/sip:')[1].split()[0].split(':')[0]
            rtt = line.split('/sip:')[1].split()[-1]
    return ip, rtt


def main():
    peers = subprocess.Popen(['asterisk', '-rx', 'pjsip list endpoints'],
                             stdout=subporcess.PIPE, encoding='utf-8')
    peers = list(peers.communicate())
    print('<<<new_asterisk_peers>>>')
    for peers in peers[0].split('\n')[4:-4]:
        try:
            peer.split('   ')
            name = peer.split('   ')[0].split([0])
            host = peer.split('   ')[0].split([-1])
            status = [i for i in peer.split('   ') if i != '']
            if status[-2].strip(' ') == 'In use':
                channels_command = f"asterisk -rx 'pjsip show channels'"
                channels = subprocess.Popen([channels_command], shell=True,
                                            stdout=subprocess.PIPE,
                                            encoding='ISO-8859-1')
                channels = list(channels.communicate())
                for channel in channels:
                    if channel is not None:
                        for line in channel.split('\n'):
                            if host.split('/')[0] in line and 'Channel:' in line:
                                time = line.split()[-1]
                                channel_id = line.split()[1].split('/')[:-1]
                                channel_id = '/'.join(channel_id)
                                channel_id_command = f"asterisk -rx 'pjsip show channel {channel_id}'"
                                calls = subprocess.Popen([channel_id_command],
                                                         shell=True,
                                                         stdout=subprocess.PIPE,
                                                         encoding='utf-8')
                                calls = list(calls.communicate())
                                for call in calls:
                                    if call is not None:
                                        b_number = call.split('CLCID:')[-1].split(' <')[-1].replace('>', '').strip()
                                        if not b_number:
                                            b_number = 'hide'
                                        b_cid = call.split('CLCID:')[-1].split(' <')[0].lstrip(' ').replace(' ', '_').replace('"', '')
                                        if not b_cid:
                                            b_cid = 'noname'
                    else:
                        ip, rtt = ip_rtt(host)
                        print(host, status[-2], ip, rtt, time, b_number, b_cid, sep='\t')
                elif status != 'Unavailable':
                    ip, rtt = ip_rtt(host)
                    print(host, status[-2], ip, rtt, sep='\t')
                else:
                    print(host, status[-2], sep='\t')
            except:
                print('error')
                continue

if __name__ == "__main__":
    main()
