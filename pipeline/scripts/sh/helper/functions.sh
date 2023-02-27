#!/bin/bash

set -e
declare -A colors=(
    ["black"]="30"
    ["red"]="31"
    ["green"]="32"
    ["brown"]="33"
    ["blue"]="34"
    ["purple"]="35"
    ["cyan"]="36"
    ["light-gray"]="37"
)

function print_colorised {
    color=$([[ "$2" != "" ]] && echo "${colors[$2]}" || echo "${colors["green"]}")
    echo -e "\e[${color}m$1\e[0m"
}

function join_by {
    local d=${1-} f=${2-}
    if shift 2; then printf %s "$f" "${@/#/$d}"; fi
}

function read_file_to_string {
    declare -a array
    while IFS= read -r line || [[ -n "$line" ]]; do
        array+=($line)
    done <$1
    echo $(join_by "$2" ${array[*]})
}
