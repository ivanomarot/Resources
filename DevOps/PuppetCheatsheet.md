Puppet Cheatsheet
---
***

Overview
---

Puppet works on the client-server model. The server is used to distribute information to the nodes to ensure that node configurations are consistent. 

Puppet is a stand alone application. In the events that the nodes lose contact with the master for a longer period of time, they do cache last known good configuration, they will continue to apply configuration until they communicate again with master.

Installation
---

Puppet master 


Login puppet master host. Add FQDN to /etc/hosts if required.

```
vi /etc/hosts
127.0.0.1 g1scott.mylabserver.com localhost
```

Run the installer

```
/root/pupper-enterprise-2016.2.1-el-7-x86_64/puppet-enterprise-installer
```


Select the Guided install.

Open the UI at `https://\<FQDN\>:3000/` 

Choose: Monolithic Installation

Install on this server

Introduce Pupper MasterFQDN

Application Orchestration

Install PostgreSQL on the PuppetDB host for me


[ Deploy Now ]


Puppet agent installation:
---

```
curl -k https://linux4vuppala2.mylabserver.com:8140/packages/current/install.bash | sudo bash
```

Puppet configuration and log files
---

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

Puppet Server
---

Manage certificates in Puppet Master:

```
puppet cert list
puppet cert list --all
puppet cert sign <name>
puppet cert sign --all
puppet cert clean <name> # removes cert
```


Puppet agent
---

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

Show all installed packages:

```
puppet resource package
```

Install or remove package:

```
puppet resource package apache ensure=present/absent
```

Show all managed resources

```
puppet resource
```

Modules
---

Print modulepath:

```
puppet config print modulepath
```

Modules help:

```
puppet help module
```

Search available modules: (PuppetForge)

```
puppet module search 'nginx'
```

Manage modules in Puppet master

```
puppet module list
puppet module install <name>
puppet module uninstall <name>
puppet module upgrade <name>
puppet module changes
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
