#!/usr/bin/env groovy
def recursiveDirCmd = "ls -R ${args[0]}"
println "Running command ${recursiveDirCmd}..."
StringBuilder standard = new StringBuilder(450000)
StringBuilder error = new StringBuilder(450000)
def result = recursiveDirCmd.execute()
result.waitForProcessOutput(standard, error)
println standard
