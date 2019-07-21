
# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/bionic64"

  config.vm.define :web, primary: true do |web|
    web.vm.hostname = "netmesh-web"
    web.vm.network "private_network", ip: "192.168.40.10"
    web.vm.network "forwarded_port", guest: 8000, host: 9000
    web.vm.network "forwarded_port", guest: 80, host: 9080
    web.vm.network "forwarded_port", guest: 443, host: 9443
    web.vm.provision "shell",
    run: "always",
    inline: "route add -net 10.64.0.0 netmask 255.255.255.0 gw 192.168.40.60 || true"
    config.vm.provider "virtualbox" do |v|
      v.memory = 512
      v.cpus = 1
    end
    web.vm.synced_folder "../netmesh", "/home/vagrant/netmesh"
  end

  config.vm.define :db do |db|
    db.vm.hostname = "netmesg-db"
    db.vm.network "private_network", ip: "192.168.40.20"
    #db.vm.provision "ansible" do |ansible|
    #    ansible.playbook = "ansible/postgres.dev.yml"
    #    ansible.verbose = true
    #end
    config.vm.provider "virtualbox" do |v|
      v.memory = 512
      v.cpus = 1
    end
  end

end
