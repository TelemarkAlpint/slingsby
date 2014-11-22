# -*- mode: ruby -*-

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  config.vm.box = "trusty-salt"

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  # The trusty-salt box is just a plain ubuntu 14.04 box that has got a recent salt installed,
  # you're recommended to update it whenever you necessary
  config.vm.box_url = "http://org.ntnu.no/telemark/dev/trusty-with-salt.box"

  # Share the salt config with the guests
  config.vm.synced_folder "salt", "/srv/salt/"
  config.vm.synced_folder "pillar", "/srv/pillar"

  # Increase available ram a notch
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "2048"]
  end

  config.vm.define "web" do |web|
    web.vm.provision :salt do |salt|
      salt.minion_config = "salt/vagrant-minion-web"
      salt.run_highstate = true
      salt.install_type = "git"
      salt.install_args = "v2014.1.10"
      salt.verbose = true
    end
    web.vm.network "private_network", ip: "10.10.10.10"
  end

  config.vm.define "fileserver" do |fileserver|
    fileserver.vm.provision :salt do |salt|
      salt.minion_config = "salt/vagrant-minion-fileserver"
      salt.run_highstate = true
      salt.install_type = "git"
      salt.install_args = "v2014.1.10"
      salt.verbose = true
    end
    fileserver.vm.network "private_network", ip: "10.10.10.11"
  end

end
