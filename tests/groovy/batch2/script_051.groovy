/*******************************************************************************
 * © 2007-2023 - LogicMonitor, Inc. All rights reserved.
 ******************************************************************************/

import com.santaba.agent.groovyapi.snmp.Snmp
import com.santaba.agent.groovyapi.win32.WMI
import com.santaba.agent.util.PortScanner

import java.time.Instant

// To run in debug mode, set to true
Boolean debug = false

String hostname = hostProps.get("system.hostname")
Integer portTimeoutInMs = 5000

// Scanned ports, these will be scanned through the script.
List<Integer> scannedPorts = [
    22,   // ssh
    80,   // http
    443,  // https
    9100, // OpenMetrics node exporter
    1433, // MS-SQL
    1521, // Oracle
    135,  // DCOM
    25,   // SMTP
    587,
    143,  // IMAP
    993
]

List<Integer> sslPorts = [
    443,   // HTTPS
    465,   // SMTP
    563,   // NNTP
    636,   // LDAP
    695,   // IEEE-MMS
    989,   // FTP
    990,   // FTP Control
    993,   // IMAP
    994,   // IRC
    995,   // POP3
    1521,  // Oracle DB/Docker Rest API
    2083,  // cPanel
    2087,  // WebHost Manager
    5223,  // XMPP
    6619,  // OSAUT
    6679,  // IRC Secure
    6697,  // IRC Secure
    5671,  // AMQP
    8443,  // Apache Tomcat
    11214  // Memcached
]

hostProps.get("exclude.ports", "").tokenize(',').each { port->
    if(port.isNumber()) {
        def portAsInt = port.toInteger()
        def index = scannedPorts.indexOf(portAsInt)
        if(index >= 0) {
            scannedPorts.remove(index)
        }

        index = sslPorts.indexOf(portAsInt)
        if(index >= 0) {
            sslPorts.remove(index)
        }
    }
}

// List of known enterprise OIDs.
def enterprises = [
    "232"  : "HP",
    "318"  : "APC",
    "664"  : "ADTRAN, Inc.",
    "674"  : "Dell",
    "1588" : "Brocade",
    "1981" : "EMC",
    "2636" : "Juniper Networks",
    "3375" : "F5 Networks, Inc.",
    "4413" : "Broadcom Corporation",
    "4526" : "Netgear",
    "5528" : "NetBotz",
    "5951" : "Netscaler",
    "6411" : "Overland",
    "6876" : "VMWare, Inc.",
    "8072" : "Ubiquiti Networks",
    "8741" : "SonicWall, Inc.",
    "10002": "Frogfoot Networks",
    "10418": "Avocent",
    "10704": "Barracuda Networks",
    "12356": "Fortinet",
    "14823": "Aruba",
    "14988": "MikroTik",
    "17095": "Microchip Technology, Inc.",
    "19746": "Data Domain Systems, Inc.",
    "25053": "Ruckus Wireless",
    "25461": "Palo Alto Networks, Inc.",
    "25506": "H3C",
    "26769": "United Technologies",
    "29671": "Meraki",
    "30065": "Arista",
    "41112": "Ubiquiti Networks",
    "44194": "EnGenius",
    "46606": "Cisco Systems, Inc.",
    "50114": "CloudGenix"
]

// Calculate the age in days
createdOn = hostProps.get("system.resourceCreatedOn")
createdOn = createdOn.isInteger() ? (createdOn as int) : null
if (createdOn) {
    println "lm.age=${(Instant.now().getEpochSecond() - createdOn)/86400}"
}

// Check for network access
start_date = new Date()
println "lm.last_check_time=${start_date.toString()}"

// Honor reserved TLDs https://datatracker.ietf.org/doc/html/rfc2606
if (hostname.endsWith(".invalid") || hostname.endsWith(".test") || hostname.endsWith(".example")) {
    println "network.resolves=false"
    return 0
}

def records

try {
    records = InetAddress.getAllByName(hostname)
    println "network.resolves=true"
    println "network.names=${records.collect{it.hostName}.join(",")}"
}
catch (Exception e) {
    println "network.resolves=false"
    println "network.error=${e.message}"
    return 0
}


// Check if device doesn't want to be probed
if (hostProps.get("lm.basicinfo.noauth") != null) {
    return 0
}

// Get sysinfo
String sysInfo = hostProps.get("system.sysinfo")
if (sysInfo == null) sysInfo = ""

// Check if Fortigate since they don't return sysinfo by default
def sysCategories = hostProps.get("system.categories")
def isFortigate   = (sysCategories.toString() + sysInfo.toString()).toLowerCase().contains("fortigate")

// if (!sysInfo) return 0 // If this device doesn't have a sysInfo device WMI or SNMP will work, looks like we are done.
String manufacturer = ""

// Add sysInfo strings for windows devices that identify as something else. Usually azure/cloud versions.
List windowsLikeSysInfo = ["Microsoft Azure Stack HCI"]

if (sysInfo.contains("Windows") || windowsLikeSysInfo.contains(sysInfo)) {
	LMDebugPrint("\n*DEBUG* Identified as Windows or Windows-like\n", debug)
    def namespace = "CIMv2"
    def session = WMI.open(hostname)
    def bios
    // BIOS
    try {
        bios = session.queryFirst(namespace, "Select * from Win32_BIOS", 10)
        println "wmi.operational=true"
    }
    catch (Exception e) {
        println "wmi.operational=false"
        println "wmi.error=${e.message}"
        return 0
    }

    println "bios.serial_number=${bios.SERIALNUMBER}"
    println "bios.version=${bios.SMBIOSBIOSVERSION}"

    // OS
    def os = session.queryFirst(namespace, "Select * from Win32_OperatingSystem", 10)
    println "os.architecture=${os.OSARCHITECTURE}"
    println "os.version=${os.VERSION}"
    println "os.version.major=${os.VERSION.split('\\.')[0]}"
    println "os.version.minor=${os.VERSION.split('\\.')[1]}"
    println "os.version.description=${os.CAPTION}"
    println "os.service_pack=${os.CSDVERSION}"

    // Processor
    def processor = session.queryAll(namespace, "Select name, NUMBEROFCORES,NUMBEROFLOGICALPROCESSORS, manufacturer,CAPTION,ADDRESSWIDTH, MAXCLOCKSPEED from win32_processor", 10)

    def core_count = 0
    def logical_core_count = 0
    def get_NAME = null
    def get_CAPTION  = null
    def get_MANUFACTURER = null
    def get_ADDRESSWIDTH = null
    def get_MAXCLOCKSPEED = null

    // iterate over each processor entry.
    processor?.each { entry ->
        // captures all core counts, and adds to our core_count variable.
        if (entry?.NUMBEROFCORES?.toInteger() > 0) {
            def new_core_count = core_count + entry.NUMBEROFCORES.toInteger()
            core_count = new_core_count
        }

        // captures all logical core counts, and adds to our logical_core_count variable.
        if (entry?.NUMBEROFLOGICALPROCESSORS?.toInteger() > 0) {
            def new_logical_core_count = logical_core_count + entry.NUMBEROFLOGICALPROCESSORS.toInteger()
            logical_core_count = new_logical_core_count
        }

        // the following can/will be overwritten as most systems will have duplicate data across the CPUs.
        get_NAME = entry.NAME
        get_CAPTION  = entry.CAPTION
        get_MANUFACTURER = entry.MANUFACTURER
        get_ADDRESSWIDTH = entry.ADDRESSWIDTH
        get_MAXCLOCKSPEED = entry.MAXCLOCKSPEED
    }

    println "processor.name=${get_NAME}"
    println "processor.caption=${get_CAPTION}"
    println "processor.manufacturer=${get_MANUFACTURER}"
    println "processor.address_width=${get_ADDRESSWIDTH}"
    println "processor.max_clock_speed=${get_MAXCLOCKSPEED}"
    println "processor.cores_count=${core_count}"
    println "processor.logical_processors_count=${logical_core_count}"


    // Computer System
    def computerSystem = session.queryFirst(namespace, "Select * from win32_computersystem", 10)
    println "os.domain=${computerSystem.DOMAIN}"
    println "endpoint.model=${computerSystem.MODEL}"
    println "endpoint.caption=${computerSystem.CAPTION}"
    println "os.computer_name=${computerSystem.NAME}"
    println "os.primary_owner_name=${computerSystem.PRIMARYOWNERNAME}"
    println "memory.total=${computerSystem.TOTALPHYSICALMEMORY}"
    println "memory.total.mb=${(Long) (Long.valueOf(computerSystem.TOTALPHYSICALMEMORY) / 1024 / 1024)}"

    manufacturer = computerSystem?.MANUFACTURER

    // First IP Address
    def networkAdapter = session.queryFirst(namespace, "SELECT * from Win32_NetworkAdapterConfiguration where IPEnabled = 'True'", 10)
    def ipAddress = networkAdapter.IPADDRESS.split(',')[0]

    println "network.address=${ipAddress}"
    println "network.network_mask=${networkAdapter.IPSUBNET.split(',')[0]}"
    println "network.mac_address=${networkAdapter.MACADDRESS}"
    println "network.type=${getIpAddressType(ipAddress)}"

}
else if (sysInfo.length() || isFortigate) {
	LMDebugPrint("\n*DEBUG* SysInfo present on non-Windows device or device recognized as Fortigate\n\t(${sysInfo})\n", debug)
    // We don't know what this is probe as SNMP
    Boolean snmpWorks = false

    // Flag to fall back to basic model oid
    Boolean modelFound = false

    try {
        sysName = Snmp.get(hostname, "1.3.6.1.2.1.1.5.0")
        snmpWorks = true
        println "snmp.operational=true"
    }
    catch (Exception e) {
        println "snmp.operational=false"
        println "snmp.exception=${e.toString()}"
    }

    if (snmpWorks) {
        // Use SysOid to determine manufacturer
        String sysObjectId = hostProps.get("system.sysoid") // sysObjectId
        def oidNumbers = sysObjectId.split("\\.")

        if (oidNumbers.length > 6) {
            // Definitive list: https://www.iana.org/assignments/enterprise-numbers/enterprise-numbers
            // Actual strings used reflect those present in the ServiceNow core_company table for the purposes of sync
            def enterpriseNumber = oidNumbers[6]
            println "enterprise_number=${enterpriseNumber}"

            manufacturer = enterprises[enterpriseNumber] ?: ""

            if (enterpriseNumber.toInteger() == 8072 && !sysInfo.contains("UAP")) {
                manufacturer = ""
            }
        }

        // Linux
        def linuxMatcher = sysInfo =~ /^Linux (?<sysname>.+?) (?<version>.+?) (?<osName>.+?) (?<processorArchitecture1>.+?) .+ (?<processorArchitecture2>.+?)$/

        if (linuxMatcher.matches()) {
            println "os.architecture=" + linuxMatcher.group('processorArchitecture2')
        }

        def cores = snmpGetMap(hostname, "1.3.6.1.2.1.25.3.3.1.2")

        if (cores) {
            println "processor.number_of_cores=${cores.size()}"
        }

        // Computer System
        def totalPhysicalMemoryKiloBytes = snmpGetBigInt(hostname, ".1.3.6.1.4.1.2021.4.5.0")


        // Section below correponds to discovery of physical properties of the device.
        //If the device is present in allowedDevice or enabled through host property, then the physical properties are discovered.
        def allowedDevices = ["Cisco", "HP", "Arista", "Fortigate", "Juniper", "Palo Alto"]
        def enablePhysDiscovery = hostProps.get("deviceBasicInfo.entPhysical.enable") ?: "false" as Boolean 
        def filteredDevice

        allowedDevices.each { device ->
            def comparator = manufacturer ?  manufacturer.toLowerCase(): (sysCategories.toString() + sysInfo.toString()).toLowerCase()
            if (comparator.contains(device.toLowerCase())) {
                filteredDevice = device
            }
        }

        //flag for Cisco-specific optimization
        def isCisco = (sysCategories.toString() + sysInfo.toString()).toLowerCase().contains("cisco")

        // Not all devices respond to the following OID.  To prevent excess queries on devices that will not be successful,
        // the following is limited to only devices known to respond (allowedDevices) and devices explicitly included via 
        // host property deviceBasicInfo.entPhysical.enable=true
        if (filteredDevice || enablePhysDiscovery) {
            LMDebugPrint("\n*DEBUG* Identified as a device that should be queried with additional OIDs.", debug)
            LMDebugPrint("\tdeviceBasicInfo.entPhysical.enable: ${enablePhysDiscovery}", debug)
            LMDebugPrint("\tIncluded devices: ${filteredDevice}", debug)

            Map<String,String> allEntities = snmpGetMap(hostname, "1.3.6.1.2.1.47.1.1.1.1")

            // Find un-contained nodes, sort them and pick the lowest id.
            def parentField = allEntities.findAll { k, v ->
                k.tokenize(".")[0] == "4" // Filter for the parent field.
            }
            def topLevelNode = parentField.findAll { k, v ->
                v.replace(" ", "") == "0"  // When the parent is 0, this entity is un-contained
            }.sort().keySet().collect{it.split("\\.")[-1]}[0]

            // If null, proceed to next parentField linked to current topLevelNode.
            if (allEntities."11.${topLevelNode}" == "") {
                topLevelNode = parentField.findAll { k, v ->
                    v.replace(" ", "") == topLevelNode
                }.sort().keySet().collect{it.split("\\.")[-1]}[0]
            }

            // Walk the whole entPhysicalEntry and sort by oid. Then we pick the lowest defined OID.
            def entWalk = allEntities.findAll { k, v -> return !v.isEmpty() }.sort()
            //for cisco devices the top level device needs to be found from the nodes that are not contained in anything else
            //however some of the information (i.e. entphysical.softwareRevision) isn't always on the top level, so we will need to go back and find those after
            if (isCisco) {
                def filtWalk = entWalk.findAll{ k, v ->
                    k.split("\\.")[-1] == topLevelNode
                }
                def keyFound = filtWalk.keySet().collect{ it.split('\\.')[0] }
                def keyPoss = entWalk.keySet().collect{ it.split('\\.')[0] }.unique(false)

                //these are oids that respond on a different level than the root node. Lets go back through and get the data
                filtWalk += (keyPoss - keyFound).collect {
                    LMDebugPrint("\t*DEBUG* OID node (${it}) was not found at the root level, defaulting to the first value returned from the entWalk", debug)
                    entWalk.find { k, v ->
                        k.split("\\.")[0] == it
                    }
                }
                entWalk = filtWalk
            }

            def seenOidTypes = []
            Boolean serialFound = false
            entWalk.each { key, value ->
                if (["",null].contains(value)) return  // When we find a blank/null entry skip it.

                def oidType = key.tokenize('.')[0]

                // Only do this once per oidType
                if (seenOidTypes.contains(oidType)) {
                    // Already seen
                    return
                }

                // New one - add to seenOidTypes
                seenOidTypes.push(oidType)

                switch (oidType) {
                    case "1":
                        println "entPhysical.Index=${value}"
                        break
                    case "2":
                        println "entPhysical.Descr=${value}"
                        break
                    case "3":
                        println "entPhysical.VendorType=${value}"
                        break
                    case "4":
                        println "entPhysical.ContainedIn=${value}"
                        break
                    case "5":
                        println "entPhysical.Class=${value}"
                        break
                    case "6":
                        println "entPhysical.ParentRelPos=${value}"
                        break
                    case "7":
                        println "entPhysical.Name=${value}"
                        break
                    case "8":
                        println "entPhysical.HardwareRev=${value}"
                        println "hardware_version=${value}"
                        break
                    case "9":
                        println "entPhysical.FirmwareRev=${value}"
                        println "firmware_version=${value}"
                        break
                    case "10":
                        println "entPhysical.SoftwareRev=${value}"
                        break
                    case "11":
                        // commented out until time to evaluate some serial numbers are incorrect
                        //println "entPhysical.SerialNum=${value}"
                        //println "endpoint.serial_number=${value}"
                        serialFound = true
                        break
                    case "12":
                        println "entPhysical.MfgName=${value}"
                        if (!manufacturer) {
                            manufacturer = value
                        }
                        break
                    case "13":
                        println "entPhysical.ModelName=${value}"
                        println "endpoint.model=${value}"
                        modelFound = true
                        break
                    case "14":
                        println "entPhysical.Alias=${value}"
                        break
                    case "15":
                        println "entPhysical.AssetID=${value}"
                        break
                    case "16":
                        println "entPhysical.IsFRU=${value}"
                        break
                    case "17":
                        println "entPhysical.MfgDate=${value}"
                        break
                    case "18":
                        println "entPhysical.Uris=${value}"
                        break
                    default:
                        // Ignore
                        break
                }
            }

            if(!serialFound && isCisco) {
                String serialNo = snmpGetString(hostname, "1.3.6.1.4.1.9.5.1.2.19.0")
                println "entPhysical.SerialNum=${serialNo}"
                println "endpoint.serial_number=${serialNo}"
            }
        }

        // SNMP Basics
        if (!modelFound) println "endpoint.model=${snmpGetString(hostname, '1.3.6.1.2.1.1.1.0').replace('\n', '\\n').replace('\r', '\\r')}"
        println "endpoint.uptime=${snmpGetString(hostname, '1.3.6.1.2.1.1.3.0')}"
        println "system_name=${snmpGetString(hostname, '1.3.6.1.2.1.1.5.0')}"

        if (totalPhysicalMemoryKiloBytes > 0) {
            println "memory.total=${(totalPhysicalMemoryKiloBytes * 1024)}"
            println "memory.total.mb=${((Long) (totalPhysicalMemoryKiloBytes / 1024))}"
        }

        // IP General
        println "ip.v4.routing_enabled=" + (snmpGetBigInt(hostname, ".1.3.6.1.2.1.4.1.0") == 1 ? "true" : "false")
        println "ip.default_ttl=" + snmpGetBigInt(hostname, ".1.3.6.1.2.1.4.2.0")
        println "ip.reassembly_timeout=" + snmpGetBigInt(hostname, ".1.3.6.1.2.1.4.13.0")
        println "ip.v6.routing_enabled=" + (snmpGetBigInt(hostname, ".1.3.6.1.2.1.4.25.0") == 1 ? "true" : "false")

        def ipAdEntAddrType = ""
        def ipAdEntAddr = ""
        def ipAdEntIfIndex = ""
        def ipAdEntNetMask = ""
        def ipAdEntBcastAddr = ""

        // First IP Address
        def ipWalk = snmpGetMap(hostname, ".1.3.6.1.2.1.4.20.1").findAll { k, v -> !v.isEmpty() }.sort()

        ipWalk.each { key, value ->
            def (oidType, ipAddress) = key.split(/\./, 2)

            // Determine the IP address type
            def ipAddressType = getIpAddressType(ipAddress)

            // Is it a management address?
            if (ipAddressType == 'management') {
                // Yes - ignore
                return
            }

            // Is the ipAdEntAddrType set?
            if (!ipAdEntAddr) {
                // No.  Set it.
                ipAdEntAddrType = ipAddressType
            }

            switch (oidType) {
                case '1':
                    ipAdEntAddr = ipAdEntAddr ?: value
                    return
                case '2':
                    ipAdEntIfIndex = ipAdEntIfIndex ?: value
                    return
                case '3':
                    ipAdEntNetMask = ipAdEntNetMask ?: value
                    return
                case '4':
                    ipAdEntBcastAddr = ipAdEntBcastAddr ?: value
                    return
                default:
                    return
            }
        }

        println "network.address=${ipAdEntAddr}"
        println "network.network_mask=${ipAdEntNetMask}"

        // detect binary MACs and convert them to hex format
        def mac = snmpGetString(hostname, ".1.3.6.1.2.1.2.2.1.6.${ipAdEntIfIndex}")
        if (mac.length() == 6) {
            byte[] macByte = mac
            def rawMacString = macByte?.encodeHex()?.toString()
            if (rawMacString && rawMacString.size() == 12) {
                def formattedMac = rawMacString.split("(?<=\\G..)").join(":")
                if (formattedMac) {
                    mac = formattedMac
                }
            }
        }

        println "network.mac_address=" + mac
        println "network.type=${ipAdEntAddrType}"
    }
}

if (manufacturer != "") {
    if (manufacturer.toLowerCase().contains("cisco")) {
        manufacturer = "Cisco Systems, Inc"
    }

    println "endpoint.manufacturer=${manufacturer}"
}

hostProps.toProperties().each { String k, String v ->
    if(k.toLowerCase().startsWith("system.")) return
    if(k.toLowerCase().endsWith(".port") || k.toLowerCase().endsWith(".ports")) {
        // Value is a list of ports
        if (v?.contains(",")) {
            v.tokenize(",").each {
                try {
                    scannedPorts << it.toInteger()
                } catch (NumberFormatException ignored) {}
            }
        }
        else {
            try {
                scannedPorts << v.toInteger()
            } catch (NumberFormatException ignored) {}
        }
    }
}

// Combine port lists and remove duplicates
scannedPorts.addAll(sslPorts)
scannedPorts = scannedPorts.unique()
List<Integer> listeningPorts = PortScanner.getInstance().scan(records[0], scannedPorts, portTimeoutInMs)

if (listeningPorts) {
    println "network.listening_tcp_ports=${listeningPorts.join(",")}"

    // Reduce sslPorts list to only ones that were found to be listening in port scan
    sslPorts.retainAll(listeningPorts)
    if (sslPorts) {
        println "network.listening_ssl_ports=${sslPorts.join(",")}"
    }
}

return 0


/**
 * Helper function to print out debug messages for troubleshooting purposes.
 * @param message
 * @param debug
 */
void LMDebugPrint(message, Boolean debug=false) {
    if (debug) {
        println(message.toString())
    }
}


/**
 * Retrieve value using SNMP GET.
 * @param hostname
 * @param oid
 * @return
 */
def snmpGetString(hostname, oid) {
    try {
        return Snmp.get(hostname, oid)
    }
    catch (IOException ignored) {
        return ""
    }
}

/**
 * Retrieve value using SNMP GET and convert to BigInteger.
 * @param hostname
 * @param oid
 * @return
 */
def snmpGetBigInt(hostname, oid) {
    def value = snmpGetString(hostname, oid)
    return (value.isBigInteger() ? value.toBigInteger() : -1)
}

/**
 * Retrieve values using SNMP Walk-As-Map.
 * @param hostname
 * @param oid
 * @return
 */
def snmpGetMap(hostname, oid) {
    try {
        return Snmp.walkAsMap(hostname, oid, null, 30000)
    }
    catch (IOException ignored) {
        return [:]
    }
}

/**
 * Convert IP address to a type.
 * @param ipAddress
 * @return
 */
def getIpAddressType(ipAddress) {
    if (ipAddress =~ /(^192\.168\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^[fF][cCdD])/) {
        return "private"
    }
    if (ipAddress =~ /(^127\.)|(^::1$)/) {
        return "management"
    }

    return "public"
}