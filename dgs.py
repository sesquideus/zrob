Target(r'output/(?P<module>\w+)/(?P<competition>\w+)/(?P<volume>\d{2})/languages/(?P<language>)/booklet.pdf')
    .requires(t"build/{module}/{competition}/{volume}/languages/{language}/(?P<problem>\w+)/problem.tex")
    .add_actions(['xelatex'])


Target(r'build/(?P<path>.*)/(?P<kind>problem|solution).md")
    .requires(t"source/{path}/meta.yaml")
    .add_actions(['render.py', '-o', self.target])

