FROM quay.io/pypa/manylinux1_x86_64:latest

MAINTAINER Anthon van der Neut <a.van.der.neut@ruamel.eu>

RUN echo '[global]' > /etc/pip.conf
RUN echo 'disable-pip-version-check = true' >> /etc/pip.conf

RUN echo 'cd /src' > /usr/bin/makewheel
RUN echo 'rm -f /tmp/*.whl'                               >> /usr/bin/makewheel
RUN echo 'for PYVER in $*; do'                            >> /usr/bin/makewheel
RUN echo '  for PYBIN in /opt/python/cp$PYVER*/bin/; do'  >> /usr/bin/makewheel
RUN echo '     echo "$PYBIN"'                             >> /usr/bin/makewheel
RUN echo '     ${PYBIN}/pip install -Uq pip'            >> /usr/bin/makewheel
RUN echo '     ${PYBIN}/pip wheel . -w /tmp'            >> /usr/bin/makewheel
RUN echo '  done'                                         >> /usr/bin/makewheel
RUN echo 'done'                                           >> /usr/bin/makewheel
RUN echo ''                                               >> /usr/bin/makewheel
RUN echo 'for whl in /tmp/*.whl; do'                      >> /usr/bin/makewheel
RUN echo '  echo processing "$whl"'                       >> /usr/bin/makewheel
RUN echo '  auditwheel show "$whl"'                       >> /usr/bin/makewheel
RUN echo '  auditwheel repair "$whl" -w /src/dist/'       >> /usr/bin/makewheel
RUN echo 'done'                                           >> /usr/bin/makewheel
RUN chmod 755 /usr/bin/makewheel

CMD /usr/bin/makewheel 27 35 36 37
