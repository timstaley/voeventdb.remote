{%- extends 'basic.tpl' -%}
{% from 'mathjax.tpl' import mathjax %}

{% block body %}

{#  Leave all the CSS imports alone.
    Quite wasteful but not worth cleaning up for this quick hack.  #}
{% for css in resources.inlining.css -%}
    <style type="text/css">
    {{ css }}
    </style>
{% endfor %}

{#  Kill the divs that break the RTD responsive page behaviour. #}
{#    <div tabindex="-1" id="notebook" class="border-box-sizing">#}
{#    <div class="container" id="notebook-container">#}
{{ super() }}
{#    </div>#}
{#      </div>#}


{%- endblock body %}


