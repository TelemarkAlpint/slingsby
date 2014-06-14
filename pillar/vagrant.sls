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
  media_url: /media/
  fileserver: localhost
  fileserver_media_root: /srv/ntnuita.no/media

# vagrant fileserver key
FILESERVER_KEY: '-----BEGIN RSA PRIVATE KEY-----

    MIIEpAIBAAKCAQEAoyOL+iiEDqQE78dTGr5QVTS3ZdVGgJbKYqSJwq4sAENwPXf1

    x9BlsgVzaKOi5i+uYlOjsHNcS8VrlB3YIcSdXeV2gThzoSdma5+vvOVyEl8Ks6Ni

    o9TMUqcuwwduL+vyUH0x/+F0Hy8L9bm2WcFUfcnM/CTkQRXODwiz/aypgpGoE/T2

    ZPZy9BV87NOu2NM2V4nbAczXmNWRzoQ3AJVbfXq+yk4231+3686v0xq/O0wfJq6s

    9xrOgVWpYa4PT3fmsVhzAwgjcgD+DhLLzwSieo82F8Uskb0n4/qBfv77d0CyF3bi

    rm8LA/4IyMFMEUJO66C+umiyRgDD2iT1QGW7eQIDAQABAoIBAQCR8MbUL1KT1l8k

    MehCUGaFEvfN/ZFoj3zV6ePjaPSr96h9FMemzONs8jtgLKMZ0SXriG8y9sBmeGHY

    yyoCa2VsDk6JIvst+5VASkZoccoubR+hvFQNw9xVRIIsroUAEc9f+d+0zPeYvfmx

    BUX/3Ve8f78FAeu/3cXM5Tg/gyrRRhZxXB+XHcHuHsWOH/9YavBIRFZ8Urb3O0g6

    YVy9UrQ4msq2zNyVrgdZBx5zaduEZK33F92fOgK8DwyUHpkb7kYtZET17PxUbpIA

    mAOrkF5r52hUy89XZmstkcO2CQy+Gx3U9oGp8Znhe1JizvFaHL0ZAKeByYDFiYf1

    yzfpurGRAoGBANReqbXO9htdgvV4hNBiRvQVCcf0AcQRA+fnJ68QzHb9wZ6oA/1r

    YFeOC/2lorgPVsz+Q6C4DL6n6Wbru3PbrMfdx5IT7TzH/Bf5lFIkBsYo3SVpbzq9

    T14cKnnbT0FDBquPRJ1XkBSRAH+ZaHIX+CrRi08H5xLxVroeq0ZZUrTbAoGBAMSn

    pEpD9Rbk+XVAMza8Fnb1VSF+1A6UQzIG5fC4pZZBBjlCuewsFBG4gN5j/x17xv2b

    Dq8n+98Fy92z4suK9MSLvB1FB5LfjrH/+ub9ZXXqGK1ePFs0uqCqXFi3u/EEJKow

    SclCLUgAkKK2BaR4fFwAzX3MmKGoa96p+lkj4Tc7AoGAeyZ524gshynu61H8Eqsq

    4hfhGCaTb5M+ZJhTFt3y832rbcmYprhBogQpR+lpNrsOZsl7hhO0sErGunwws7rL

    swsU08ziYcDGm1CLhiaGFxtTQoKlkbZ98+D5cLiQeRPZJltqOqOwVXzQgS4At0jX

    DF1/H1FB2mZBGKT4RU8++skCgYEAiO9/LCOED4wj1Kx+vPdd4TnWLLvG59v/ql85

    UFUTILxonAjFtBnBY9GJEtKou5wMJV4KbJc4AMVlfxyaqUc6R35R4EPIEVLQZ0wr

    Jxt9wgzfYCGFf7EI34WhRjmyihJrgYKcbqNBKqkSDesXpL4tQldgv99uzOqdKnBM

    HjQoyC8CgYA9SvLiRwzWfeAE9/qMwU8mrvrLr+CN1yNGHWv3b+8o2VqsjWGNMupn

    xhm0wyTPOrjpOwdKYPsAWd4tFwaFmA3A8HXurjcXqZ17Dii6/2rAoJoGosFzgqFH

    NSddVYNEowsH3azzX3txUGhHu/uxwykUGE0HKTkSjJaZHFjqtTu0eA==

    -----END RSA PRIVATE KEY-----

    '
