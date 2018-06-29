#!/usr/bin/env python3
'''
    Copyright (c) 2017-2018 HERE Europe B.V.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    SPDX-License-Identifier: Apache-2.0
    License-Filename: LICENSE
'''
import re
import sys

result_array = []


def array_from_string(string):
    ''' As input a string delimited by , (comma)
    Return only not empty string and remove none value
    '''
    match = re.split(',|\n', string)
    return [x for x in match if x and x != "none"]


def popemptyvalue(array):
    ''' Pop empty values '''
    # for i in x:
    #    if i == "":
    #        x.pop()
    return [x for x in array if x]


def findconfcomp():
    ''' Find apache config in the input file '''
    infile = sys.stdin.read()
    regex = r"Module Name: (.*)\nContent handlers:(.*)\nConfiguration Phase Participation: (.*)\nRequest Phase Participation: (.*)\nModule Directives:[\s]+((.*?\n)+?)(Current Configuration:((.*?\n)+?\n|\n)|(\n))"
    prog = re.compile(regex, re.MULTILINE)
    i = 1
    for result in prog.finditer(infile):
        print(i)
        module_name = result.group(1)
        print("Module name %s" % module_name)
        conf_phase = array_from_string(result.group(3))
        print("Configuration Phase Participation: %s" % (len(conf_phase)))
        req_phase = array_from_string(result.group(4))
        print("Request Phase Participation: %s" % (len(req_phase)))
        try:
            currentconf = array_from_string(result.group(8))
            print("Current Configuration: %s \n" % (len(currentconf)))
        except:
            currentconf = []
            print("Current Configuration: %s \n" % (len(currentconf)))
        i = i + 1
        result_array.append(
            {"module_name": module_name, "conf_phase":
             len(conf_phase), "req_phase": len(req_phase),
             "current_conf": len(currentconf)})


def module_to_remove(array):
    ''' If no configuration is present for the module consider it removable
    '''
    remove_array = []
    work_array = list(array)
    i = 0
    for x in work_array:
        if x["current_conf"] == 0:
            remove_array.append(x['module_name'])
        else:
            pass
        i = i + 1
    return remove_array


def array_subtraction(array, toremarray):
    ''' Remove toremarray from array '''
    for x in toremarray:
        i = 0
        for y in array:
            if y['module_name'] == x:
                print("POPPED: ", y['module_name'])
            i = i + 1
    return [j['module_name'] for j in array]


if __name__ == "__main__":
    findconfcomp()
    remove_array = module_to_remove(result_array)
    print("To remove safely:\n", remove_array)
    print("\nTo KEEP: ", array_subtraction(result_array, remove_array))
