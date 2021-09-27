FROM gitpod/workspace-full
USER root
RUN true \
	&& apt-get -q update \
	&& apt-get install -yq \
		gettext \
	&& apt-get autoremove -yq \
	&& rm -rf /var/lib/apt/lists/*


	&& apt -q update \
	&& apt install -yq \ 
		libdmtx0a \
	&& rm -rf /var/lib/apt/lists/*
