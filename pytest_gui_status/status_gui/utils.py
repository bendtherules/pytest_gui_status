import jinja2
import os


def render_template(app, tmpl_name, tmpl_params):
    with open(os.path.join(app.template_path, tmpl_name)) as f_tmpl:
        tmpl_content = f_tmpl.read()
    return jinja2.Template(tmpl_content).render(tmpl_params)
