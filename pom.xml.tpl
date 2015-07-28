<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
        <!-- General information -->
{% block attributes %}
    <groupId>{{ groupId }}</groupId>
    <artifactId>{{ artifactId }}</artifactId>
    <version>{{ version }}</version>
    <name>Ariane Community Installer</name>
    <packaging>{{ packaging }}</packaging>
{% endblock %}
{% block modules %}
    <modules>
        {%- for mod in modules %}
        <module>{{mod.name}}</module>
        {% endfor -%}
    </modules>
{% endblock %}
<repositories>
        <repository>
            <id>nexus.echinopsii.net</id>
            <name>echinopsii.net repository</name>
            <url>http://nexus.echinopsii.net/nexus/content/groups/public/</url>
            <releases>
                <enabled>true</enabled>
            </releases>
            <snapshots>
                <enabled>true</enabled>
                <updatePolicy>always</updatePolicy>
            </snapshots>
        </repository>
    </repositories>

</project>
