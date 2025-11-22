#!/usr/bin/env python

from zrob import SystemCallTarget, Action, Builder, Prereq, Output, Optional


build_xelatex = Action('xelatex', '-file-line-error', '-shell-escape', '-jobname={outname}', '-halt-on-error', '-synctex=1', '-interaction=nonstopmode', '{infile}')
texfot_xelatex = Action('texfot')


render = Action('render.py', Prereq('source'), Output, '--context', Prereq('meta'),
                Optional(Prereq('preamble'), '--preamble', Prereq('preamble')))


booklet = SystemCallTarget(r'output/(?P<module>\w+)/(?P<competition>\w+)/(?P<volume>\d{2})/languages/(?P<language>)/booklet.pdf') \
    .requires(tex=r"build/{module}/{competition}/{volume}/languages/{language}/(?P<problem>\w+)/problem.tex") \
    .add_action(build_xelatex)


standalone = \
    SystemCallTarget(
        r'build/(?P<path>.*)/(?P<kind>problem|solution).md'
    ).requires(
        source="source/{path}/{kind}.md",
        meta="source/{path}/meta.yaml",
    ).optional(
        preamble="source/{path}/preamble.md",
    ).add_action(
        render
    )


builder = Builder()

builder.register(standalone)
builder.build()
