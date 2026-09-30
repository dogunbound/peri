#!/bin/bash
leftwm state -w 0 -t "$(cd "$(dirname "$0")" && pwd -P)/../templates/workspaces-template.liquid"
