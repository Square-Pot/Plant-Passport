FROM gitpod/workspace-full

RUN sudo apt-get update  && sudo apt-get install -y   gettext    libdmtx0a   && sudo rm -rf /var/lib/apt/lists/*
