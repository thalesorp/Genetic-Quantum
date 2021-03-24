#!/bin/bash
#
# Generate a statistical summary for the given data vector
#
# Version 0.5
# (c) 2008 Everthon Valadao <everthonvaladao@gmail.com> under the GPL
#          http://www.gnu.org/copyleft/gpl.html
#

sed 's/,/\./g' "$@" | nice "${JAVA_HOME}"/usr/bin/java -Xms512m -Xmx1536m -jar statistics.jar /dev/stdin
