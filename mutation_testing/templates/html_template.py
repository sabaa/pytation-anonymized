HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Pattern Locations</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        h1 {
            color: #333;
        }
        h2 {
            color: #420420;
        }
        p {
            margin-bottom: 10px;
        }
        a {
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        code {
            display: block;
            padding: 10px;
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            margin-top: 10px;
            white-space: pre-wrap;
            line-height: 1.5;
            font-size: 14px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h1>Pattern Locations</h1>

    <h2> Static Patterns </h2>
    {% for entry in data_static %}
    <p>{{ entry['operator_name'] }} -
        <a href="#" onclick="showCode('{{ entry['pattern_location']['filename'] }}', {{ entry['pattern_location']['start_line'] }}); return false;">
            {{ entry['pattern_location']['filename'] }} : {{ entry['pattern_location']['start_line'] }} - {{ entry['pattern_status'] }}
        </a>
    </p>
    <code id="{{ entry['pattern_location']['filename'] }}-{{ entry['pattern_location']['start_line'] }}" style="display:none;">
        {{ get_code(entry['pattern_location']['filename'], entry['pattern_location']['start_line']) }}
    </code>

    {% endfor %}

    <h2> Dynamic Patterns </h2>
    {% for entry in data_dynamic %}
    <p>{{ entry['operator_name'] }} -
        <a href="#" onclick="showCode('{{ entry['pattern_location']['filename'] }}', {{ entry['pattern_location']['start_line'] }}); return false;">
            {{ entry['pattern_location']['filename'] }} : {{ entry['pattern_location']['start_line'] }} - {{ entry['pattern_status'] }}
        </a>
    </p>
    <code id="{{ entry['pattern_location']['filename'] }}-{{ entry['pattern_location']['start_line'] }}" style="display:none;">
        {{ get_code(entry['pattern_location']['filename'], entry['pattern_location']['start_line']) }}
    </code>
    {% endfor %}

    <script>
        function showCode(filename, startLine) {
            var codeId = filename + '-' + startLine;
            var codeElement = document.getElementById(codeId);
            codeElement.style.display = (codeElement.style.display === 'none' || codeElement.style.display === '') ? 'block' : 'none';
        }
    </script>
</body>
</html>
'''
