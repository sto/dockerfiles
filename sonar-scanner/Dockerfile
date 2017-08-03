FROM openjdk:8
# Dockerfile for sonar-scanner
#
# Initial version from https://github.com/newtmitch/docker-sonar-scanner
#
# Build
# -----
# $ docker build -t sonar-scanner .
# 
# RUN
# ---
# $ docker run --interactive --tty --rm=true -e "LANG" \
#              -u "$(id -u):$(id -g)"                  \
#              -v "$(pwd):/source"                     \
#              -v "/etc/group:/etc/group:ro"           \
#              -v "/etc/passwd:/etc/passwd:ro"         \
#              -v "/etc/shadow:/etc/shadow:ro"         \
#              sonar-scanner $CMND

MAINTAINER Sergio Talens-Oliag <sto@iti.es>
ENV URL=https://sonarsource.bintray.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-3.0.3.778-linux.zip

# update distribution and packages
RUN echo '# See /etc/apt/sources.list.d/' > /etc/apt/sources.list \
  && echo 'deb http://httpredir.debian.org/debian stretch main' \
     > /etc/apt/sources.list.d/debian-stretch.list \
  && echo 'deb http://security.debian.org/ stretch/updates main' \
     >> /etc/apt/sources.list.d/debian-stretch.list \
  && apt-get update \
  && apt-get dist-upgrade -y --no-install-recommends \
  && apt-get install -y aptitude \
  && aptitude -y purge ~o \
  && apt-get purge aptitude -y \
  && apt-get autoremove --purge -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install required packages
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
                     git \
                     curl \
                     tmux \
                     htop \
                     maven \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set timezone to Europe/Madrid
ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
	&& echo $TZ > /etc/timezone

# Install sonarscanner from the web
RUN cd /opt \
    && curl --insecure -L $URL -o /tmp/sonarscanner.zip \
    && unzip /tmp/sonarscanner.zip \
    && rm -f /tmp/sonarscanner.zip \
    && ln -sf sonar-scanner-* sonar-scanner

ENV SONAR_RUNNER_HOME=/opt/sonar-scanner
ENV PATH=$PATH:/opt/sonar-scanner/bin

COPY sonar-runner.properties /opt/sonar-scanner/conf/sonar-scanner.properties

WORKDIR /source
VOLUME  /source

CMD sonar-scanner -Dsonar.projectBaseDir=/source
