#!/bin/bash
sed 's/,/\./g' "$@" | nice "${JAVA_HOME}"/usr/bin/java -Xms512m -Xmx1536m -jar statistics.jar /dev/stdin
