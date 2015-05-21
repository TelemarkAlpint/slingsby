# Never run this state without also configuring ssh rules to prevent being locked out
include:
    - ssh

# Set chain to ACCEPT in the beginning of a run (before flush) to not drop any
# existing connections. Causes a race condition in between the states, but I
# considered this good enough since the highstate is executed at a random time
# and would be hard to exploit.
iptables-default-policy-before-configuration:
    iptables.set_policy:
        - table: filter
        - chain: INPUT
        - policy: ACCEPT
        - hardfail: True # If this fails, stop execution, as we should definitely not flush the rules now
        - order: 1

# We need an early flush since salt doesn't detect modification to defined
# rules, and will thus add duplicates if anything is changed. We thus start
# from a clean slate every run to prevent any issues from this.
iptables-flush-existing:
    iptables.flush:
        - order: 1


iptables-log-nonmatched-input:
    iptables.append:
        - table: filter
        - chain: INPUT
        - jump: LOG
        - match:
            - comment
            - limit
        - comment: "iptables: Log all non-matching packets"
        - limit: 10/min
        - log-prefix: 'iptables.default: '
        - save: True
        - order: last


iptables-default-policy:
    iptables.set_policy:
        - table: filter
        - chain: INPUT
        - policy: DROP
        - save: True
        # Make sure that the DROP policy is always added as the last step, to
        # prevent firewalling off the current session before all the other
        # rules have been applied
        - order: last


# Allow all traffic on local interface
iptables-allow-lo:
    iptables.append:
        - table: filter
        - chain: INPUT
        - if: lo
        - jump: ACCEPT
        - match: comment
        - comment: "iptables: Allow traffic to lo"
        - save: True


{% for proto in ('udp', 'tcp') %}
# Allow incoming established traffic (typically replies to outgoing requests)
iptables-allow-incoming-{{ proto }}:
    iptables.append:
        - table: filter
        - chain: INPUT
        - match:
            - state
            - comment
        - connstate: ESTABLISHED
        - proto: {{ proto }}
        - comment: "iptables: Allow incoming established {{ proto }} traffic"
        - jump: ACCEPT
        - save: True
{% endfor %} # end udp/tcp


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
        - comment: "iptables: Allow incoming {{ icmp_msg_text }}"
        - limit: 90/min
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


# Split iptables related logs to /var/log/iptables.log
iptables-rsyslog-config:
    file.managed:
        - name: /etc/rsyslog.d/11-iptables.conf
        - contents: |
            :msg, startswith, "iptables" -/var/log/iptables.log
            & stop
            :msg, regex, "^ *\[ *[0-9]*\.[0-9]*\] iptables" -/var/log/iptables.log
            & stop


    service.running:
        - name: rsyslog
        - watch:
            - file: iptables-rsyslog-config


# Rotate the logs
iptables-logrotate-config:
    file.managed:
        - name: /etc/logrotate.d/iptables
        - contents: |
            /var/log/iptables.log {
                daily
                missingok
                rotate 14
                compress
                notifempty
            }


# Make sure config is persisted to disk and restored on reboot
iptables-persistent:
    pkg.installed
