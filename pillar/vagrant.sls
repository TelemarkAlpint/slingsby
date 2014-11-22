# Add a key pair for vagrant so that we can use passwordless login
developers:
  vagrant:
    fullname: vagrant
    groups:
      - admin
    ssh_keys:
      - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCjI4v6KIQOpATvx1MavlBVNLdl1UaAlspipInCriwAQ3A9d/XH0GWyBXNoo6LmL65iU6Owc1xLxWuUHdghxJ1d5XaBOHOhJ2Zrn6+85XISXwqzo2Kj1MxSpy7DB24v6/JQfTH/4XQfLwv1ubZZwVR9ycz8JORBFc4PCLP9rKmCkagT9PZk9nL0FXzs067Y0zZXidsBzNeY1ZHOhDcAlVt9er7KTjbfX7frzq/TGr87TB8mrqz3Gs6BValhrg9Pd+axWHMDCCNyAP4OEsvPBKJ6jzYXxSyRvSfj+oF+/vt3QLIXduKubwsD/gjIwUwRQk7roL66aLJGAMPaJPVAZbt5 vagrant@vagrant-ubuntu-trusty-64

env:
  db_uri: localhost

slingsby:
  bind_url: ntnuita.local
  secret_key: verysecretindeed
  db_password: notthatsecret
  media_url: http://media.ntnuita.local/
  fileserver: fileserver@10.10.10.11
  fileserver_media_root: /srv/fileserver/

# vagrant fileserver key
FILESERVER_KEY: '-----BEGIN RSA PRIVATE KEY-----

    MIIEpgIBAAKCAQEA9kW6aPG0poX/ix/eWKp0Pv/FSUYcGINO8MtwJhiCDS301J7l

    jmEsvP5lAxIn+pCB/L9PpuVIRs6e4asWloHLmMqkyfMlmENaVIsP+Sqjj0BFtCVl

    6s3MQhl3NIlqmZpIegDR8zn6zl+PyTx6/OEQMGlGCrGMkkI6aXgImZJN5Z3fOC4Q

    tryf33zw0ZA3PgnxwzzMP7E8TF1QVMH4uH4xeJIJHm+qlPxYDbtVglhTZqegoR6y

    0ujdp1qoSlIKWJLsCJr35mAABlpWSczCpfzyYWdE9WD5KpNbCDZ/dZYVB49D7eH3

    fTxw8Fu9qt88sdvo8VSc2EKDf4xXLch1tO7sawIDAQABAoIBAQCz7dn2FrJQABLm

    iNAgo9jutlxj3q9kUXt5folfrARIsMzyE23QirrvEkam6br/3Fi8WuJNI7Oc2BVI

    94E3UXl5FoUzb0yGZJ84qalv+HErll/W8IP3+4hCuuxXHBcgRpKxYKwEMtZFtZgO

    BPwuihkT5bZg1bvImE6pBCP0X+o92Z11xjPFcsYTFNwqUqC6MqUms7rnns/0pW1Z

    WopvD8Ogb/z+jgYxljhXmaBj5W6SRP76qXqrLPnksLbRUSONQ8S1pYVpCKCeJRU+

    6xXDO5k+xlHS9sw2yGFwoXL6PkcnX0qX2o6fOLn8KEnzkEiF+czVv2txY92idUDW

    N8hJxuNxAoGBAPznPFEY5qi79Qng7aReXzO9436EnkxB5n4SRNew+p4bh+BHN3Sl

    WPDuZ9U69UYmZDVPe3t6ZMR8qQUSxt17xSajUcSGSKdoeTu78qhZEKnu2eFcufWM

    +N3eBYffQBhmjGqSDAhTaGJ88FWepuVIyKmAOFj+1dc2IBaLKlD4HDq/AoGBAPlJ

    tP5anfKS3GQjL+WZxT4t70DGPSqZL7Ebff8MnQrmHV37Vb2Zg9kp5tQis0oICAuW

    MsXN8qsd3qsQv/YyrrrFHW3EQHvbR6RHgw722R5hIAdtR0jVV7iPCt7H/3kurgAr

    BCWJylc+ZwWRAQFEQfNHQb+HxtzSBUW9FFn1clVVAoGBAOWvHJiKhPG5wlG2dh1R

    mCTl0DaXOy0GrM7SyLMbiIEPf9ew1iyZ/qzR2HtPkHKla1z/UqZSAjJxBRAWfYWp

    YuQ0b46MZm+j8nbNuxQpz3iF9Fs4W6sm3N6jRWKg3xVKDTy8ZzEojyTjU2JvNCQI

    djV6vbIVvyA1h+7xdP0UWI8BAoGBANeNYC8/c6u4SVFdC6FgoSju1x4PS/x1kMN3

    ni7XXUN7TpFhLfZPs64niSyNBLJS14INUcGwHtDPdyY7yYC8ulFM9/Fd7NQr+3qV

    S0G5OGwIV4WUfDsCHmO7bA7OqJzEPDhw+Zjr2EYv8yzhARlzSANv7e4LHWz7PQvc

    Pqi6jy4xAoGBAJ1gRpeR04gXRqOSjwxanz5fNmqnlMaMIvbdibEn53g4jBmbFl6O

    t+Xc8xPmZmxKYqRq0FUJNLx9SfrdLstsNeIyEEoxJaSLiLlHaChdlzdCXTzhh7Kl

    7Tbr6c8kYDLjYgRvGp87zKbSuwyZ81uDHkzglL30fTq4V5//FGoP7/KH

    -----END RSA PRIVATE KEY-----

    '
