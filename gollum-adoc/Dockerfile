FROM ruby:stretch
#
# Docker to process gollum wikis with asciidoctor support
#
# Build
# -----
# $ docker build -t stodh/gollum-adoc .
# 
# RUN
# ---
# $ docker run --interactive --tty --rm=true -e "LANG" \
#              -p 127.0.0.1:4567:127.0.0.1:4567        \
#              -u "$(id -u):$(id -g)"                  \
#              -v "$(pwd):/documents"                  \
#              -v "/etc/group:/etc/group:ro"           \
#              -v "/etc/passwd:/etc/passwd:ro"         \
#              -v "/etc/shadow:/etc/shadow:ro"         \
#              gollum-adoc $CMND
LABEL maintainer="Sergio Talens-Oliag <sto@iti.es>"
# Update distribution sources.list (use httpredir mirror)
RUN echo '# See /etc/apt/sources.list.d/' > /etc/apt/sources.list \
  && echo 'deb http://httpredir.debian.org/debian stretch main' \
     > /etc/apt/sources.list.d/debian-stretch.list \
  && echo 'deb http://security.debian.org/ stretch/updates main' \
     >> /etc/apt/sources.list.d/debian-stretch.list
# Install common required packages
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
                     git \
                     sudo \
                     python-docutils \
                     python-pygments \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# Asciidoctor w/ syntax highliters
RUN gem install asciidoctor \
                coderay \
                pygments.rb \
                rouge
# Add gollum support (GitLab Wiki tool)
RUN apt-get update \
  && apt-get install -y libicu-dev cmake \
  && gem install github-linguist \
                 github-markdown \
				 gollum \
  && apt-get purge -y libicu-dev cmake \
  && apt-get autoremove --purge -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# Update distribution packages (it is done the last step to make sure that it
# is executed each time the container is built)
RUN apt-get update \
  && apt-get dist-upgrade -y --no-install-recommends \
  && apt-get install -y aptitude \
  && aptitude -y purge ~o \
  && apt-get purge aptitude -y \
  && apt-get autoremove --purge -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# All installed!
WORKDIR /documents
VOLUME  /documents
# Expose gollum default port
EXPOSE 4567
# By default we simply run a bash shell
CMD ["/bin/bash"]
