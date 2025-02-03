{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{user}}
{% endblock %}

{% block html %}
welcome to Website , your Token is {{token.access}}
{% endblock %}