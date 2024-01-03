#!/bin/bash

mkdir wiktionary_sayings
# seed link:
next_page_link="/w/index.php?title=Category:English_idioms&from=AA"

while [ ! -z "${next_page_link}" ]; do
    html_content="$(curl -s "https://en.wiktionary.org${next_page_link}")"

    while IFS= read line; do
        filename="$(echo ${line} | cut -d '=' -f5-)"
        echo "${filename}"
        content="$(curl $line | xpath -q -e '//mediawiki/page/revision/text' | grep -Pzoe "(?s){{trans-top\|.*}}\n(.*?){{trans-bottom" | sed -re 's/\*:? //g' | cut -d ":" -f2- | sed -re 's/ \{\{t\+?//g' -re 's/\}\}//g' | sed -re 's/\|([a-z]+)\|(.+)(\|impf.*?|\|tr=.*)?/\1 \2/g;s/\{\{qualifier.*|\|impf|\|tr=.*//g;s/^ .*$//g;s/\{\{trans-.*//g;s/\[|\]//g;s/,\|/\n/g;s/([a-z]+)\|(.+)(\|.*?)?/\1 \2/g' | grep -Pv "^$|\-" | sed -re 's/\|/ /g;s/\{\{.*//;s/([a-z]+)([. ]+)(lit=.*)?/\1 \2/g' | sed 's/  / /g' | sed -re 's/([a-z]+) (.*) alt=(.*?)/\1 \2\n\1 \3/g' | sort -h)"
        [ -z "$content" ] || printf "${content}" > ./wiktionary_sayings/$filename
        echo $content
        sleep 12
    done< <(echo "$html_content" | grep '<li><a href="/wiki/' | grep -v Category | sed -re 's/.*href=\"(.*)\".*title=\".*/\1/g;s|/wiki/||g;s|^|https://en.wiktionary.org/w/api.php?format=json\&action=query\&origin=*\&export\&exportnowrap\&titles=|g' )
    next_page_link=$(echo "$html_content" | grep -oP '<a href="\K[^"]*(?="[^>]*>next page</a>)' | sed -e "s/&amp;/\&/g" | head -n 1)
    echo "${next_page_link}"
done
