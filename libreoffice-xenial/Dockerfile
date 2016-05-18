FROM ubuntu:xenial
#
# Build
# -----
# $ docker build -t libreoffice-xenial .
# 
# RUN
# ---
# $ docker run --interactive --tty --rm=true -e "DISPLAY" -e "LANG"   \
#              -u "$(id -u):$(id -g)"                                 \
#              -v "/etc/group:/etc/group:ro"                          \
#              -v "/etc/passwd:/etc/passwd:ro"                        \
#              -v "/etc/shadow:/etc/shadow:ro"                        \
#              -v "/etc/sudoers.d:/etc/sudoers.d:ro"                  \
#              -v "/tmp/.X11-unix:/tmp/.X11-unix:rw"                  \
#              -v "$HOME:$HOME" -w "$HOME"                            \
#              --ipc=host --name libreoffice stodh/libreoffice-xenial
#
MAINTAINER Sergio Talens-Oliag <sto@iti.es>
# update distribution and packages
RUN sed -i -e 's/^deb-src/#deb-src/' /etc/apt/sources.list \
  && apt-get update \
  && apt-get dist-upgrade -y --no-install-recommends \
  && apt-get install -y aptitude \
  && aptitude -y purge ~o \
  && apt-get purge aptitude -y \
  && apt-get autoremove --purge -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# install catalan and spanish lang packs
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
             language-pack-ca language-pack-es \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# install packages
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
             libreoffice \
             libreoffice-help-ca libreoffice-l10n-ca \
             myspell-ca hyphen-ca mythes-ca \
             libreoffice-help-es libreoffice-l10n-es \
             myspell-es hyphen-es mythes-es \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# Command
CMD ["libreoffice"]
