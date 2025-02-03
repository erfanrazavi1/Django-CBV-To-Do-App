{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello Your resetpassword link is: 
{% endblock %}

{% block html %}
http://localhost:8000/accounts/api/v1/token/reset-password/confirm/{{token.access}}
{% endblock %}