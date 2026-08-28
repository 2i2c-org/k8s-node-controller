# Helm chart repository for k8s-node-controller

This is a bare Helm chart repository specifically for the [k8s-node-controller](https://github.com/2i2c-org/k8s-node-controller) chart.

{% for chartmap in site.data.index.entries %}
## Releases: {{ chartmap[0] }}

| Version | Date | App. version |
|---------|------|---------------------|
  {%- assign sortedcharts = chartmap[1] | sort: 'created' | reverse %}
  {%- for chart in sortedcharts %}
| [{{ chart.version }}]({{ chart.urls[0] }}) | {{ chart.created | date_to_long_string }} | {{ chart.appVersion }} |
  {%- endfor %}
{%- endfor %}