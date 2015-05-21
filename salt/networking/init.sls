{% if grains.get('hostname') %}
hostname:
  cmd.run:
    - name: hostname {{ grains.get('hostname') }}
{% endif %}

web-host:
  host.present:
    - ip: 10.10.10.10
    - name: ntnuita.local

fileserver-host:
  host.present:
    - ip: 10.10.10.11
    - name: media.ntnuita.local

vagrant-firewall:
  iptables.append:
    - table: filter
    - chain: INPUT
    - match:
      - comment
    - proto: tcp
    - comment: "networking: Allow SSH on vagrant ports"
    - dports: 22,2222,2200,2201,2202
    - jump: ACCEPT
    - save: True
