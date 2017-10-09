FROM ruby:2.4
#
# Docker to process jekyll and asciidoctor documents
#
# Build
# -----
# $ docker build -t jekyll-adoc .
# 
# RUN
# ---
# $ docker run --interactive --tty --rm=true -e "LANG" \
#              -p 127.0.0.1:4000:127.0.0.1:4000        \
#              -u "$(id -u):$(id -g)"                  \
#              -v "$(pwd):/documents"                  \
#              -v "/etc/group:/etc/group:ro"           \
#              -v "/etc/passwd:/etc/passwd:ro"         \
#              -v "/etc/shadow:/etc/shadow:ro"         \
#              jekyll-adoc $CMND
MAINTAINER Sergio Talens-Oliag <sto@iti.es>
# update distribution and packages -- use httpredir mirror
RUN echo '# See /etc/apt/sources.list.d/' > /etc/apt/sources.list \
  && echo 'deb http://httpredir.debian.org/debian jessie main' \
     > /etc/apt/sources.list.d/debian-jessie.list \
  && echo 'deb http://security.debian.org/ jessie/updates main' \
     >> /etc/apt/sources.list.d/debian-jessie.list \
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
                     node \
                     sudo \
                     python-pygments \
                     python-docutils \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# Install jekyll >= 3.5.0 (we want liquid >= 4.0)
RUN gem install jekyll --version '>= 3.5.0'

# Default jekyll components (list taken from
# https://github.com/jekyll/docker/blob/master/opts.yml)
RUN gem install html-proofer \
                jekyll-sitemap \
                jekyll-mentions \
                jekyll-coffeescript \
                jekyll-sass-converter \
                jekyll-redirect-from \
                jekyll-paginate \
                jekyll-compose \
                jekyll-feed \
                jekyll-docs \
                RedCloth \
                kramdown \
                jemoji \
                minima \
                github-pages \
                jekyll-github-metadata
# Extra jekyll packages used by us
RUN gem install jekyll-archives \
                jekyll-paginate-v2 \
                jekyll-postfiles \
                # For our theme
                autoprefixer-rails \
                bootstrap-sass \
                sass \
                # Syntax Highlighters
                pygments.rb \
                rouge
# Jekyll admin
RUN gem install jekyll-admin
# Asciidoctor
RUN gem install asciidoctor \
                coderay \
                jekyll-asciidoc
# additional packages
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
                     graphviz \
                     fonts-liberation \
                     linkchecker \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# Add diagram support to jekyll and asciidoctor
RUN gem install asciidoctor-diagram \
                jekyll-plantuml
# Add python-blogdiag (there are packages @ sid, but we install it from pip
# for now)
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
                     python-pip \
                     python-dev \
                     python-setuptools \
  && pip install blockdiag \
  && apt-get purge -y \
                      python-pip \
                      python-dev \
                      python-setuptools \
  && apt-get autoremove -y --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# Install gems from pre
RUN gem install asciidoctor-epub3 \
                asciidoctor-pdf \
                --pre
# Install gems from git
RUN cd /tmp \
    && git clone https://github.com/sto/jekyll-rst.git \
    && cd jekyll-rst && rake install && rake clobber \
    && cd .. && rm -rf jekyll-rst

WORKDIR /documents
VOLUME  /documents
EXPOSE 4000

CMD ["/bin/bash"]
