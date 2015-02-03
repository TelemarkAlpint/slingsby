swap-file:
  cmd.run:
    - name: |
        [ -f /.swapfile ] || dd if=/dev/zero of=/.swapfile bs=1M count=2048
        chmod 0600 /.swapfile
        mkswap /.swapfile
        echo '/.swapfile      none      swap     sw       0       0' >> /etc/fstab
        swapon -a
    - unless: file /.swapfile 2>&1 | grep -q "Linux/i386 swap"
