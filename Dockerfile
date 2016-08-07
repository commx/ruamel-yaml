FROM quay.io/pypa/manylinux1_x86_64

MAINTAINER Anthon van der Neut <a.van.der.neut@ruamel.eu>

RUN echo 'cd /src' > /usr/bin/makewheel
RUN echo 'rm -f /tmp/*.whl'                         >> /usr/bin/makewheel
RUN echo 'for PYBIN in /opt/python/$1*/bin/; do'    >> /usr/bin/makewheel
RUN echo '  echo "$PYBIN"'                          >> /usr/bin/makewheel
RUN echo '  ${PYBIN}/pip wheel . -w /tmp'           >> /usr/bin/makewheel
RUN echo 'done'                                     >> /usr/bin/makewheel
RUN echo ''                                         >> /usr/bin/makewheel
RUN echo 'for whl in /tmp/*.whl; do'                >> /usr/bin/makewheel
RUN echo '  auditwheel repair "$whl" -w /src/dist/' >> /usr/bin/makewheel
RUN echo 'done'                                     >> /usr/bin/makewheel
RUN chmod 755 /usr/bin/makewheel

RUN yum install -y libyaml-devel


CMD /usr/bin/makewheel
