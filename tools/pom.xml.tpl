<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    {% block attributes %}
    <parent>
        <groupId>{{ groupId }}</groupId>
        <artifactId>{{ artifactId }}</artifactId>
        <version>{{ version }}</version>
        <relativePath>..</relativePath>
    </parent>

    <groupId>{{ artifactId }}</groupId>
    <artifactId>{{ artifactId }}.{{ name }}</artifactId>
    <name>Ariane Community Installer Tools</name>
    {% endblock %}

    <dependencies>
        <dependency>
            <groupId>org.apache.sshd</groupId>
            <artifactId>sshd-core</artifactId>
            <version>0.11.0</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.1</version>
                <configuration>
                    <showDeprecation>true</showDeprecation>
                    <showWarnings>true</showWarnings>
                    <optimize>true</optimize>
                </configuration>
            </plugin>
            <plugin>
                <!-- This plugin takes care of packaging the artifact as an OSGi Bundle -->
                <groupId>org.apache.felix</groupId>
                <artifactId>maven-bundle-plugin</artifactId>
                <version>2.4.0</version>
                <configuration>
                    <instructions>
                        <Embed-Dependency>*;scope=compile|runtime</Embed-Dependency>
                        <Embed-Transitive>true</Embed-Transitive>
                    </instructions>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-javadoc-plugin</artifactId>
                <version>2.9</version>
                <executions>
                    <execution>
                        <id>attach-javadocs</id>
                        <goals>
                            <goal>jar</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>