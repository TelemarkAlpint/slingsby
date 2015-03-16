{% set ssh = pillar.get('ssh', {}) %}

# Drop incoming traffic from private ranges (probably spoofed)
# Note that 10.0/8, 172.16/16 and 192.168/16 are allowed, otherwise private
# networking wouldn't work. These should be blocked on public interfaces
# though.
{% for source_range in (
    '224.0.0.0/4',
    '240.0.0.0/5',
    '127.0.0.0/8',
    ) %}
iptables-drop-incoming-private-traffic-{{ source_range }}:
    iptables.append:
        - table: filter
        - chain: INPUT
        - if: eth*
        - match: comment
        #- comment: "iptables: Block spoofed addresses"
        - comment: onewordcomment
        - s: {{ source_range }}
        - jump: DROP
        - order: 2
        - save: True
{% endfor %}


{% for ip_family in ('ipv4', 'ipv6') %}

# Set chain to ACCEPT in the beginning of a run (before flush) to not drop any
# existing connections. Causes a race condition in between the states, but I
# considered this good enough since the highstate is executed at a random time
# and would be hard to exploit.
iptables-default-policy-before-configuration-{{ ip_family }}:
    iptables.set_policy:
        - family: {{ ip_family }}
        - table: filter
        - chain: INPUT
        - policy: ACCEPT
        - order: 1

# We need an early flush since salt doesn't detect modification to defined
# rules, and will thus add duplicates if anything is changed. We thus start
# from a clean slate every run to prevent any issues from this.
iptables-flush-existing-{{ ip_family }}:
    iptables.flush:
        - family: {{ ip_family }}
        - order: 1


iptables-log-nonmatched-input-{{ ip_family }}:
    iptables.append:
        - table: filter
        - family: {{ ip_family }}
        - chain: INPUT
        - jump: LOG
        - match:
            - comment
            - limit
        #- comment: "iptables: Log all non-matching packets"
        - comment: onewordcomment
        - limit: 10/min
        - save: True
        - order: last


iptables-default-policy-{{ ip_family }}:
    iptables.set_policy:
        - table: filter
        - family: {{ ip_family }}
        - chain: INPUT
        - policy: DROP
        - save: True
        # Make sure that the DROP policy is always added as the last step, to
        # prevent firewalling off the current session before all the other
        # rules have been applied
        - order: last


# Allow all traffic on local interface
iptables-allow-lo-{{ ip_family }}:
    iptables.append:
        - table: filter
        - chain: INPUT
        - family: {{ ip_family }}
        - if: lo
        - jump: ACCEPT
        - match: comment
        #- comment: "iptables: Allow traffic to lo"
        - comment: onewordcomment
        - save: True


ssh-firewall-{{ ip_family }}:
    iptables.append:
        - table: filter
        - family: {{ ip_family }}
        - chain: INPUT
        - proto: tcp
        - dport: {{ ssh.get('port', 22) }}
        - jump: ACCEPT
        - save: True


http-firewall-{{ ip_family }}:
    iptables.append:
        - table: filter
        - family: {{ ip_family }}
        - chain: INPUT
        - proto: tcp
        - sport: 80
        - jump: ACCEPT
        - save: True


{% for proto in ('udp', 'tcp') %}
# Allow incoming established traffic
iptables-allow-incoming-established-{{ ip_family }}-{{ proto }}:
    iptables.append:
        - table: filter
        - chain: INPUT
        - family: {{ ip_family }}
        - match:
            - state
            - comment
        - connstate: ESTABLISHED
        - proto: {{ proto }}
        #- comment: "iptables: Allow incoming established traffic"
        - comment: onewordcomment
        - jump: ACCEPT
        - save: True
{% endfor %}

# Block invalid packets
iptables-block-invalid-{{ ip_family }}:
    iptables.append:
        - table: filter
        - chain: INPUT
        - family: {{ ip_family }}
        - proto: tcp
        - match:
            - state
            - comment
        - connstate: INVALID
        #- comment: "iptables: Drop invalid packets"
        - comment: onewordcomment
        - target: DROP
        - save: True
        - order: 2


{% endfor %} # end ipv4/ipv6


# Allow a subset of icmp messages
{% for icmp_msg_num, icmp_msg_text in {
        '0': 'echo-reply',
        '3/1': 'destination-unreachable/host-unreachable',
        '3/3': 'destination-unreachable/port-unreachable',
        '3/4': 'destination-unreachable/fragmentation-needed',
        '8': 'echo-request',
        '11': 'time-exceeded',
    }.items() %}
iptables-allow-incoming-icmp-{{ icmp_msg_text }}:
    iptables.append:
        - table: filter
        - chain: INPUT
        - family: ipv4
        - match:
            - icmp
            - comment
            - limit
        - protocol: icmp
        - icmp-type: {{ icmp_msg_num }}
        #- comment: "iptables: Allow incoming {{ icmp_msg_text }}"
        - comment: onewordcomment
        - limit: 30/min
        - jump: ACCEPT
        - save: True
{% endfor %} # end icmp msgs


# Block kernel from ever accepting a icmp redirect
iptables-block-kernel-redirect:
    sysctl.present:
        - name: net.ipv4.conf.all.accept_redirects
        - value: 0


# Block Smurf IP DoS attack
iptables-block-kernel-smurf:
    sysctl.present:
        - name: net.ipv4.icmp_echo_ignore_broadcasts
        - value: 1


# Make sure config is persisted to disk and restored on reboot
iptables-persistent:
    pkg.installed
