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
