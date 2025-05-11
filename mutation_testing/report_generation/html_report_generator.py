import json
from jinja2 import Template
import os
import codecs

from mutation_testing.templates.html_template import HTML_TEMPLATE
from mutation_testing.constants import (
    DYNAMIC_PATTERN_FILENAME,
    STATIC_PATTERN_FILENAME,
    UNCOVERED_PATTERN_FILENAME,
    EQUIVALENT_PATTERN_FILENAME,
    HTML_REPORT_FILENAME
)


def get_json_data(filename):
    if filename is None:
        return {}
    try:
        with open(filename, 'r') as file:
            data = file.read()
        return json.loads(data)
    except FileNotFoundError:
        return {}


def generate_html_report(
        input_file_paths=None, html_output_file=HTML_REPORT_FILENAME):
    if input_file_paths is None:
        input_file_paths = {}
    json_file_static = input_file_paths.get("STATIC", STATIC_PATTERN_FILENAME)
    json_file_dynamic = input_file_paths.get("DYNAMIC", DYNAMIC_PATTERN_FILENAME)

    inputs = {
        'data_static': get_json_data(json_file_static),
        'data_dynamic': get_json_data(json_file_dynamic),
        'get_code': get_code
    }

    render_html_report(inputs, html_output_file)


def render_html_report(inputs, html_output_file):
    template = Template(HTML_TEMPLATE)
    rendered_html = template.render(**inputs)
    with open(html_output_file, "w") as html_file:
        html_file.write(rendered_html)
    print(f"HTML file generated: {os.path.abspath(html_output_file)}")


def get_code(filename, start_line):
    with codecs.open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        number_of_lines = len(lines)
        if start_line is None:
            start_line = 1
        start_range = start_line - 5 if start_line - 5 > 0 else 0
        end_range = start_line + 5 if start_line + 5 < number_of_lines else number_of_lines
        for i in range(start_range, end_range):
            lines[i] = str(i + 1) + "\t" + lines[i]

        for i in range(start_range, end_range + 1):
            if i + 1 == start_line:
                lines[i] = "<span style='background-color: #FBF719;'>" + lines[i] + "</span>"

        return ''.join(lines[start_range:end_range])


if __name__ == "__main__":
    generate_html_report()
