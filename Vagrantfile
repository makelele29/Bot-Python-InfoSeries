# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Insertar ubuntu 16 en la maquina virtual
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.synced_folder "bot", "/bot"

  config.vm.provider "virtualbox" do |v|
    # Para que tenga entorno visual
	# v.gui = true
	# Cambiar el nombre de la maquina
	v.name = "BOT"
  end
  config.vm.provision "shell", path: "config.sh"
end
