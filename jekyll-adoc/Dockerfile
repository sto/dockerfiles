FROM ruby:buster
#
# Docker to process jekyll and asciidoctor documents
#
# Build
# -----
# $ docker build -t stodh/jekyll-adoc .
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
LABEL maintainer="Sergio Talens-Oliag <sto@mixinet.net>"
# Update sources.list (use httpredir mirror)
RUN echo '# See /etc/apt/sources.list.d/' > /etc/apt/sources.list \
  && echo 'deb http://httpredir.debian.org/debian buster main' \
     > /etc/apt/sources.list.d/debian-buster.list \
  && echo 'deb http://security.debian.org/ buster/updates main' \
     >> /etc/apt/sources.list.d/debian-buster.list
# Install common required packages
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
                     git \
                     sudo \
                     python3-docutils \
                     python3-pygments \
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
                sassc \
                # Syntax Highlighters
                pygments.rb \
                rouge
# Jekyll admin
RUN gem install jekyll-admin
# Asciidoctor
RUN gem install asciidoctor \
                asciidoctor-rouge \
                coderay \
                jekyll-asciidoc
# Additional packages
# FIXME: The 'umlet' package is missing from buster, so we leave it out for now
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
# Add blockdiag support ... there is a debian package on sid, but we
# install using other tools 
RUN apt-get update \
  && apt-get install -y --no-install-recommends  \
                     python3-pip \
                     python3-setuptools \
                     python3-wheel \
  && pip3 install --system \
                 blockdiag \
                 seqdiag \
                 actdiag \
                 nwdiag \
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
# Add reveal.js support for asciidoctor
RUN gem install asciidoctor-revealjs
# Add concurrent-ruby to the image
RUN gem install concurrent-ruby
# Add bespoke support for asciidoctor
RUN gem install asciidoctor-bespoke --pre
# Install nodejs version for bespoke processing -- we keep in on 11.x for now,
# as newer versions break gulp < 4 compatibility
RUN NODEREPO="node_11.x" \
  && apt-get update \
  && apt-get install -y --no-install-recommends apt-transport-https \
  && echo "deb https://deb.nodesource.com/${NODEREPO} buster main" \
     > /etc/apt/sources.list.d/nodesource.list \
  && curl -s https://deb.nodesource.com/gpgkey/nodesource.gpg.key \
     | apt-key add - \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
                     nodejs \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# Install gulp
RUN npm install -g gulp
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
## Expose jekyll default port
#EXPOSE 4000
# By default we simply run a default shell
CMD ["/bin/sh"]
