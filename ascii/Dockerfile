FROM debian:bullseye-slim
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
             boxes \
             cmatrix \
             cowsay \
             curl \
             figlet \
             fortune fortunes \
             libaa-bin \
             libcurses-perl \
             make \
             perl \
             python3 \
             sl \
             toilet \
             unzip \
  && curl -L -s -k \
     https://github.com/nitram509/ascii-telnet-server/archive/master.zip \
     > /tmp/ascii-telnet-server-master.zip \
  && cd /opt \
  && unzip /tmp/ascii-telnet-server-master.zip \
  && rm -f /tmp/ascii-telnet-server-master.zip \
  && mv ascii-telnet-server-master ascii-telnet-server \
  && rm -rf ascii-telnet-server/screenshots \ 
  && echo '#!/bin/sh' > /usr/bin/ascii-telnet-server \
  && echo 'python3 /opt/ascii-telnet-server/ascii_telnet_server.py "$@"' \
     >> /usr/bin/ascii-telnet-server \
  && chmod +x /usr/bin/ascii-telnet-server \
  && curl -s -k \
  https://cpan.metacpan.org/authors/id/K/KB/KBAUCOM/Term-Animation-2.6.tar.gz \
     > Term-Animation-2.6.tar.gz \
  && tar xaf Term-Animation-2.6.tar.gz \
  && rm -f Term-Animation-2.6.tar.gz \
  && cd Term-Animation-2.6 \
  && perl Makefile.PL && make && make install \
  && cd .. \
  && rm -rf Term-Animation-2.6 \
  && curl -s -k https://robobunny.com/projects/asciiquarium/asciiquarium \
     > /usr/bin/asciiquarium \
  && chmod +x /usr/bin/asciiquarium \
  && apt-get purge -y --autoremove curl make unzip \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
CMD ["/bin/bash"]
