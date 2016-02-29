Overview
========

``ruamel.yaml`` is a YAML 1.2  loader/dumper package for Python. It is a
derivative of Kirill Simonov's `PyYAML 3.11
<https://bitbucket.org/xi/pyyaml>`_ 

``ruamel.yaml`` supports `YAML 1.2`_ and has  round-trip loaders and dumpers
that preserves, among others:

- comments
- block style and key ordering are kept, so you can diff the round-tripped 
  source
- flow style sequences ( 'a: b, c, d') (based on request and test by
  Anthony Sottile)
- anchors names that are hand-crafted (i.e. not of the form``idNNN``)
- `merges <http://yaml.org/type/merge.html>`_ in dictionaries are preserved

This preservation is normally not broken unless you severely alter
the structure of a component (delete a key in a dict, remove list entries).
Reassigning values or replacing list items, etc., is fine.

For the specific 1.2 differences see :ref:`yaml-1-2-support`

Although individual indentation is not preserved, you can specify both
indentation and specific offset of block sequence dashes within that
indentation. There is a utility function that tries to determine the
correct values for ``indent`` and ``block_seq_indent`` that can
then be passed to the dumper.

.. include:: links.rst
