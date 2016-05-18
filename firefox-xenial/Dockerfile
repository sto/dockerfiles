FROM ubuntu:xenial
#
# Build
# -----
# $ docker build -t firefox-xenial .
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
#              --ipc host --name libreoffice stodh/firefox-xenial
#
# NOTE: We use the --ipc host to allow the use of X11 Shared Memory, if we
# don't do it firefox fails at launch time if we don't pass additional
# arguments
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
             firefox \
             firefox-locale-ca \
             firefox-locale-es \
			 libgl1-mesa-dri \
			 libgl1-mesa-glx \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# Command
CMD ["firefox"]
