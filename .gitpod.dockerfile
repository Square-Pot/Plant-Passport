FROM gitpod/workspace-full
USER root
RUN true \
	&& apt-get -q update \
	&& apt-get install -yq \
		gettext \
    libdmtx0a \
	&& apt-get autoremove -yq \
	&& rm -rf /var/lib/apt/lists/*
