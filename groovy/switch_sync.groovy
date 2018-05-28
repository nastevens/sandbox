/**
 * Virtual / Physical Switch Sync.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy
 * of the License at:
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

definition(
    name: "Virtual / Physical Switch Sync",
    namespace: "nastevens",
    author: "Nick Stevens",
    description: "Keep switch devices with multiple switches in sync with virtual switches",
    category: "My Apps",
    iconUrl: "https://s3.amazonaws.com/smartapp-icons/Meta/light_outlet.png",
    iconX2Url: "https://s3.amazonaws.com/smartapp-icons/Meta/light_outlet@2x.png",
)

preferences {
    page(name: "numberPage", nextPage: "setupPage")
    page(name: "setupPage")
}

def numberPage() {
    dynamicPage(name: "numberPage", install: false, uninstall: true) {
        section {
            input("vNumber",
                  "number",
                  title:"Number of virtual switches",
                  defaultValue: 2,
                  required: true
            )
        }
    }
}

def setupPage() {
    dynamicPage(name: "setupPage", install: true, uninstall: true) {
        section {
            input("physical",
                  "capability.switch",
                  title: "Physical Switch",
                  multiple: false,
                  required: true
            )
            for (int i = 1; i <= vNumber; i++) {
                input("virtual${i}",
                      "capability.switch",
                      title: "Virtual Switch for Switch ${i}",
                      multiple: false,
                      required: true
                )
            }
        }
    }
}

def installed() {
  log.debug "Installed with settings: ${settings}"
  initialize()
}

def updated() {
  log.debug "Updated with settings: ${settings}"
  unsubscribe()
  initialize()
}

def initialize() {
  log.debug "Initializing Virtual / Physical Switch Sync"
  for (int i = 1; i <= vNumber; i++){
     subscribe(physical, "switch${i}", physicalHandler)
     subscribeToCommand(settings["virtual${i}"], "on", virtualHandler)
     subscribeToCommand(settings["virtual${i}"], "off", virtualHandler)
     subscribe(physical, "power${i}", powerHandler)
     subscribe(physical, "energy${i}", energyHandler)
  }
}

def virtualHandler(event) {
    log.debug "virtualHandler called with event: " +
              "deviceId ${event.deviceId} " +
              "name: ${event.name} " +
              "source: ${event.source} " +
              "value: ${event.value} " +
              "isStateChange: ${event.isStateChange()} " +
              "isPhysical: ${event.isPhysical()} " +
              "isDigital: ${event.isDigital()} " +
              "data: ${event.data} " +
              "device: ${event.device}"
    for (int i = 1; i <= vNumber; i++) {
        if (event.deviceId == settings["virtual${i}"].id) {
             physical."${event.value}${i}"()
        }
    }
}

def physicalHandler(event) {
    log.debug "physicalHandler called with event: " +
              "name: ${event.name} " +
              "source: ${event.source} " +
              "value: ${event.value} " +
              "isStateChange: ${event.isStateChange()} " +
              "isPhysical: ${event.isPhysical()} " +
              "isDigital: ${event.isDigital()} " +
              "data: ${event.data} " +
              "device: ${event.device}"
    for (int i = 1; i <= vNumber; i++){
        if (event.name == "switch${i}") {
            try {
                sendEvent(settings["virtual${i}"], [name: "switch", value: "$event.value", type: "physical"])
            } catch (e) {
                log.trace e
            }
        }
    }
}

def powerHandler(event) {
   log.debug "powerHandler called with event: " +
             "name: ${event.name} " +
             "source: ${event.source} " +
             "value: ${event.value} " +
             "isStateChange: ${event.isStateChange()} " +
             "isPhysical: ${event.isPhysical()} " +
             "isDigital: ${event.isDigital()} " +
             "data: ${event.data} " +
             "device: ${event.device}"
    for (int i = 1; i <= vNumber; i++){
        if (event.name == "power${i}") {
            sendEvent(settings["virtual${i}"], [name: "power", value: "$event.value"])
        }
    }
}

def energyHandler(event) {
   log.debug "energyHandler called with event: " +
             "name: ${event.name} " +
             "source: ${event.source} " +
             "value: ${event.value} " +
             "isStateChange: ${event.isStateChange()} " +
             "isPhysical: ${event.isPhysical()} " +
             "isDigital: ${event.isDigital()} " +
             "data: ${event.data} " +
             "device: ${event.device}"
    for (int i = 1; i <= vNumber; i++){
        if (event.name == "energy${i}") {
            sendEvent(settings["virtual${i}"], [name:"energy", value:"$event.value"])
        }
    }
}
