# Puppet Cheatsheet

## Overview

Puppet works on the client-server model. The server is used to distribute information to the nodes to ensure that node configurations are consistent. 

Puppet is a stand alone application. In the events that the nodes lose contact with the master for a longer period of time, they do cache last known good configuration, they will continue to apply configuration until they communicate again with master.

## Installation

### Puppet master 


Login puppet master host. Add FQDN to /etc/hosts if required.

```
vi /etc/hosts
127.0.0.1 g1scott.mylabserver.com localhost
```

Enable the repository:

```
sudo rpm -Uvh https://yum.puppet.com/puppet6/puppet6-release-el-7.noarch.rpm
````

Disable existing service:

````
service puppetmaster stop
````

In case Puppet runs over apache:

````
sudo mv /etc/httpd/conf.d/puppetmaster.conf ~/
service httpd restart
````

Install the Puppet server package:

````
yum install puppetserver
systemctl start puppetserver
````

### Puppet Agent

Enable the repository:

```
sudo rpm -Uvh https://yum.puppet.com/puppet6/puppet6-release-el-7.noarch.rpm
````

If necessary, add the path to run the executables:

````
export PATH=/opt/puppetlabs/bin:$PATH
````

Install the Puppet agent package:

````
yum install puppet-agent
/opt/puppetlabs/bin/puppet resource service puppet ensure=running enable=true
````


### Puppet Enterprise (Web)

Download and extract the executables.

Run the installer

````
/root/pupper-enterprise-2016.2.1-el-7-x86_64/puppet-enterprise-installer
````


Select the Guided install.

Open the UI at `https://\<FQDN\>:3000/` 

Choose: Monolithic Installation

Install on this server

Introduce Pupper MasterFQDN

Application Orchestration

Install PostgreSQL on the PuppetDB host for me


[ Deploy Now ]


Aagent installation:

```
curl -k https://linux4vuppala2.mylabserver.com:8140/packages/current/install.bash | sudo bash
```

## Puppet configuration and log files

Puppet configuration file:

```
/etc/puppetlabs/puppet/puppet.conf
```

Print all configuration settings:

```
puppet config print all
```

Check current Puppet version and if there is an update available:

```
./opt/puppetlabs/bin/puppet-enterprise-version-check
```

Puppet Server log:

```
/var/log/puppetlabs/puppetserver/puppetserver.log
```

PuppetDB log:

```
/var/log/puppetlabs/puppetdb/puppetdb.log
```

SSL certs location:

```
/etc/puppetlabs/puppet/ssl
```

Agent installation packages:

```
/opt/puppetlabs/server/data/packages/public/current
```

Site.pp location:

```
/etc/puppetlabs/code/environments/productions/manifests/site.pp
```

Environment config file: 

```
/etc/puppetlabs/code/environments/production/environment.conf
```

## Puppet Server

Apply a manifest:

````
puppet apply -l /tmp/manifest.log manifest.pp
puppet apply --modulepath=/root/dev/modules -e "include ntpd::server"
puppet apply --catalog catalog.json
````

Validate the default site manifest at /etc/puppetlabs/puppet/manifests/site.pp:
````
puppet parser validate
````

Validate two arbitrary manifest files:

````
puppet parser validate init.pp vhost.pp
````

Validate form STDIN

````
cat init.pp | puppet parser validate
````

Manage certificates in Puppet Master:

```
puppet cert list           # lists available nodes to sign
puppet cert list --all     # lists all signed nodes
puppet cert sign <name>    # manually sign specific node
puppet cert sign --all     # sign all nodes
puppet cert clean <name>   # removes cert
```

Delete the setting 'setting_name' from the 'main' configuration domain:

````
puppet config delete setting_name
````

Delete the setting 'setting_name' from the 'master' configuration domain:

````
puppet config delete setting_name --section master
````

Get puppet's runfile directory:

````
puppet config print rundir
````

Get a list of important directories from the master's config:

````
puppet config print all --section master | grep -E "(path|dir)"
````

Set puppet's runfile directory:

````
puppet config set rundir /var/run/puppetlabs
````

Set the vardir for only the agent:

````
puppet config set vardir /opt/puppetlabs/puppet/cache --section agent
````

## Puppet agent

Apply a catalog on Puppet agent (bootstrap):

```
puppet agent -t --server <puppet_master>
puppet agent -t --debug
puppet agent -t --noop --verbose  #Dry run
puppet agent -t --environment <specific_environment>
```

Disable/Enable Puppet agent

```
puppet agent --disable
puppet agent --disable <info message> # Only recent versions
puppet agent --enable
```

Manage resources

```
puppet resource                                # Show all managed resources
puppet resource package apache ensure=present  # Install package
puppet resource package apache ensure=present  # Remove package
```

## Modules

Print modulepath:

```
puppet config print modulepath
```

Modules help:

```
puppet help module
```

Manage modules in Puppet master

```
puppet module list              # lists current installed modules
puppet module install <name>    # downloads/installs modules from http://forge.puppetlabs.com
puppet module uninstall <name>  # removes/deletes module
puppet module upgrade <name>    # upgrades to new version of module
puppet module search <name>     # search modules from http://forge.puppetlabs.com
puppet module changes           # lists last changes in modules
```

Build new module with full skeleton:

```
puppet module generate author/module
```

Check for missing module dependencies:

```
puppet module list --tree
```

Build a module release package (.tar.gz)

```
puppet module build author/module
```

Module paths:

```
apache/             # main module dir
apache/manifests    # manifest code
apache/lib          # plugins, ruby code
apache/templates    # ERB templates
apache/files        # files used in module
apache/tests        # usage examples
apache/Modulefile   # metadata paths inside a module:
```

Examples:

```
content => template('mysql/my.cnf.erb'),
Template is in: $modulepath/mysql/templates/my.cnf.erb

source => 'puppet:///modules/mysql/my.cnf'
File is in: $modulepath/mysql/files/my.cnf
```

## Facter

Show all facts

````
facter   
````

Show OS Family facter 

````
facter osfamily 
````

Show facters in YAML or JSON

````
facter -y
facter -j
````

Get Puppet Enterprise version

````
facter -p | grep pe_
````

Get Puppet agent All-in-one version

````
facter -p | grep aio
````

Use fact inside a manifest using 'facter' function 

````
notify { "OS is ${::facts['operatingsystem']}": } 
````

Use fact inside manifest directly 

````
notify { "OS is $::operatingsystem": } 
````

## Puppet DSL

Declare a resource:

````
type { 'title':
  param => 'value',
}
````

Define a class:

````
class <name> (
  DataType $param1,           # this parameter must be provided upon declaration
  DataType $param2 = 'value',
) {
  # Puppet DSL code
}
````

Import a class

````
include <name>  # no ordering, the mentioned class will be somewhere in the catalog
require <name>  # strict ordering, the class must be finished prior continuing
contain <name>  # local ordering, the class must be finished within the class where the contain function is used
````

Define a class as resource type:

````
class { '<name>':
  param1 => 'value',
}
````

Self define resource type

````
define <name> (
  DataType $param1,
  DataType $param2 = 'value',
){
  # Puppet DSL
  # all resource type declaration must use the $title variable
  # older Puppet code uses $name instead of $title
}
````

Declare self define resource

````
<name> { 'title':
  param1 => 'value',
}
````

## Puppet control statements

Variable
````
$content = "some content\n" 
````

Array
````
$address = [$addr1, $addr2, $addr3]
````

Hash
````
$warning_msg = { memory => "memory low",
 disk => "disk space low"
 }
notify { $warning_msg[disk]: }
````

Complex Hash

````
$services = {
  "apache" => {
    "version" => "2.8",
    "desc" => "web server"
  },
  "mysql" => {
    "version" => "5.6",
    "desc" => "web server"
  }
}
````

Case

````
case $test_variable {
  'value1': {         # specific value
    # Puppet DSL
  }
  /regexp/: {         # regular expression
    # Puppet DSL
  }
  'value2', 'value3': {  # multiple values
    # Puppet DSL
  }
  default: {          # fall back value - optional
    # optional, Puppet DSL
  }
}
````

If
````
if $test_variable {
  # Puppet DSL
} else {  # else is optional
  # Puppet DSL
}

if $test_variable == 'content' {
  # Puppet DSL
}

if $test_variable =~ /regexp/ {
  # Puppet DSL
}
````

Selector

````
$result_var = $test_var ? {
  'value1' => 'return_val1',
  'value2' => 'return_val2',
  default  => 'return_val3',
}
````

Iterate over array
````
$var = [ 'element1', 'element2' ]
$var.each |DataType $key| {
  type { $key:
    param => 'value',
  }
}
````

Iterate over hash
````
$var = {
  'key1' => {
    'var1' => 'val1',
    'var2' => 'val2',
  },
  'key2' => {
    'var1' => 'val1',
  },
}

$var.each |DataType $key, DataType $val| {
  type { $key:
    * => $val,
}
````

## Hiera

Functions:

````
hiera() 
hiera_array() 
hiera_hash() 
hiera_include() 
````

Hiera arrays:

````
hiera ssh_users ["root", "jeff", "gary", "hunter"] 
hiera ssh_users.0 
root
````

Hiera hash

````
$ hiera user {"name"=>"kim", "home"=>"/home/kim"} 
$ hiera user.name 
kim 
````

Use Hiera for class assignment in Site.pp 

````
hiera_include() 
````

Hiera config file 

````
/etc/puppetlabs/puppet/hiera.yaml 
````

Hierarchies: 

````
:hierarchy: 
   - "nodes/%{::clientcert}" 
   - "roles/%{::role}" 
   - "%{::osfamily}" 
   - "%{::environment}" 
   - common 
````

Lookup wiht puppet command:

````
puppet lookup profile::hiera_test::backups_enabled --environment production --node jenkins-prod-03.example.com
````

Query

````
hiera <key>                                      # to query common.yaml only
hiera <key> -m <FQDN>                            # to query config of a given node (using mcollective)
hiera <key> -i <FQDN>                            # to query config of a given node (using Puppet inventory)
hiera <key> environment=production fqdn=myhost1  # to pass values for hiera.yaml
````

To dump complex data:

````
hiera -a <array key>
hiera -h <hash key>
````

## Resource ordering

Require and subscribe

````
package { 'foo':
  ensure => present,
}
file { '/etc/foo/foo.conf':
  ensure  => file,
  require => Package['foo'],
}
service { 'foo':
  ensure    => running,
  subscribe => File['/etc/foo/foo.conf'].
}
````

Before and notify

````
package { 'foo':
  ensure => present,
  before =: File['/etc/foo/foo.conf'],
}
file { '/etc/foo/foo.conf':
  ensure => file,
  notify => Service['foo'],
}
service { 'foo':
  ensure => running,
}
````

Resource chaining

````
package { 'foo':
  ensure => present,
}
file { '/etc/foo/foo.conf':
  ensure => file,
}
service { 'foo':
  ensure => running,
}

Package['foo'] -> File['/etc/foo/foo.conf'] ~> Service['foo']
````

Or multiline:

````
Package['foo']
-> File['/etc/foo/foo.conf']
~> Service['foo']
````