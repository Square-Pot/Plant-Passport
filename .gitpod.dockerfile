FROM gitpod/workspace-full

RUN sudo apt-get update  && sudo apt-get install -y gettext && sudo apt-get install -y libdmtx0a && sudo rm -rf /var/lib/apt/lists/*