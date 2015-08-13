vsh:install repository:plan/com.typesafe.akka/2.3.4
vsh:plan start com.typesafe.akka 2.3.4

vsh:install repository:plan/org.infinispan/6.0.2
vsh:plan start org.infinispan 6.0.2

vsh:install repository:plan/org.hibernate/4.3.0
vsh:plan start org.hibernate 4.3.0

vsh:install repository:plan/org.neo4j/2.1.2
vsh:plan start org.neo4j 2.1.2
{% for mod in modules -%}
{% if mod.type == 'core' %}
vsh:install repository:plan/net.echinopsii.ariane.community.core.{{mod.name}}/{{mod.version}}
vsh:plan start net.echinopsii.ariane.community.core.{{mod.name}} {{mod.version}}
{% else %}
vsh:install repository:plan/net.echinopsii.ariane.community.{{mod.name}}/{{mod.version}}
vsh:plan start net.echinopsii.ariane.community.{{mod.name}} {{mod.version}}
{% endif %}
{%- endfor %}