FROM ruby:2.4
#
# Docker to process jekyll and asciidoctor documents
#
# Right now (2017/02/12) I'm using jekyll with liquid 4.0 (whitespace control,
# finally) but the support is missing from the latest released version of
# jekyll (3.4.0), although it has been merged into the project's master
# branch; to be able to use it, the build tries to install a jekyll version >=
# 3.5.0 or it installs that same version from git using the commit that merged
# the liquid 4.0.0 support.
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
                     python-pygments \
                     python-docutils \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# Install jekyll >= 3.5.0 or use GIT
RUN gem install jekyll --version '>= 3.5.0' || ( \
      cd /tmp && \
	  git clone http://github.com/jekyll/jekyll.git && \
      cd jekyll && \
	  git checkout c01b7e4a4a70ee4df498398585bce4e6f59fb04a && \
	  gem build jekyll.gemspec && \
	  gem install jekyll-3.4.0.gem && \
	  cd .. && \
	  rm -rf jekyll \
	)
# Default jekyll components (taken from https://github.com/jekyll/docker)
RUN gem install pygments.rb \
                jekyll-sitemap \
				jekyll-archives \
				jekyll-paginate-v2 \
                jekyll-mentions \
                jekyll-coffeescript \
                jekyll-sass-converter \
                jekyll-redirect-from \
                jekyll-compose \
                jekyll-feed \
                rdiscount \
                redcarpet \
                rouge \
                kramdown \
                jemoji \
                RedCloth \
                maruku \
                html-proofer
# github-pages support              
RUN gem install github-pages jekyll-github-metadata
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
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# Add diagram support to jekyll and asciidoctor
RUN gem install asciidoctor-diagram \
                jekyll-plantuml
# Install gems from pre
RUN gem install asciidoctor-epub3 \
                asciidoctor-pdf \
				--pre
# Install gems from git
RUN cd /tmp \
    && git clone https://github.com/sto/jekyll-rst.git \
	&& cd jekyll-rst && rake install && rake clobber \
	&& cd .. && rm -rf jekyll-rst

# To move up (jekyll theme)
RUN gem install minima

WORKDIR /documents
VOLUME  /documents
EXPOSE 4000

CMD ["/bin/bash"]
