NatureBank
==========

Version 1.0 (2015-10-01)

NatureBank is a database for managing data on biotopes and landscapes
as well as species of the flora and fauna. It can be accessed through
a web application powered by Django.

The database provided with this repository is empty, containing only
indicative data of lookup tables mostly in Greek language (/db/naturebank.dump).


Requirements
------------
 * Python v.2.7
 * PostreSQL v.9.0
 * PostGIS v.2.1

Additional requirements related with Django and its applications are
documented in file requirements.txt.
NatureBank has been successfully tested with PostreSQL v.9.0,
spatially enabled with PostGIS v.2.1. Other versions of the above
software or other spatially enabled databases may work as well.


Installation
------------

The following steps are needed to manually install NatureBank.
For an automated approach using Ansible visit the [naturebank-ansible
repository](https://github.com/ellak-monades-aristeias/naturebank-ansible)

#### Install Python, PostreSQL and PostGIS
#### Install Django and dependencies
#### Create a database user
#### Create a spatially enabled database

`createdb naturebank -U postgres -W -h localhost -O filotis
     -T template_postgis`

#### Populate the database

`pg_restore -i -h localhost -U postgres -d naturebank -v
     <path>/db/<dump file>`

Use dump file */db/naturebank.dump* to install the database with
empty tables filled only with some indicative data.
After that load the fixture for the django flatpages:

`python manage.py loaddata naturebank_flatpages.json`

#### Create the configuration file

Copy file /naturebank_project/settings/local-example.py to
/naturebank_project/settings/local.py making the appropriate adjustments.

#### Configure your web server


License
-------
    NatureBank is a database for managing data on  biotopes and
    landscapes as well as species of the flora and fauna.
    Copyright (C) 2005-2015 National Technical University of Athens

    NatureBank is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public
    License along with this program. If not, see
    <http://www.gnu.org/licenses/>.

NatureBank is a reengineered, generalized version of Filotis, which is
Copyright (C) 2005-2015 National Technical University of Athens.
Filotis is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

All additional 3rd party software provided with this release and/or used
by NatureBank are AGPLv3 compatible as their licenses ensure the freedoms
to run, study, share (copy), and modify the software. Additionally, some
of them are copylefted.


Acknowledgements
----------------
NatureBank is based on Filotis, a database for the natural environment
of Greece, developed between 2005-2015 by the National Technical University
of Athens. Main authors of Filotis are Anthony Christophides and Stefanos
Kozanis. Theodore Kargas was the main author of the initial version of Filotis.
Authors of NatureBank are Antonis Christophides, George Karavokiros and
Antonis Koukouvinos.

Related Sites
-------------
The following sites and documents are related with the NatureBank project:

Description|Link
-----------|---
NatureBank, a database for managing data on biotopes and landscapes as well as species of the flora and fauna. |[naturebank](https://github.com/ellak-monades-aristeias/naturebank)
User guide for NatureBank (in Greek)|[User Guide](https://github.com/ellak-monades-aristeias/naturebank/blob/master/NatureBank_user_guide.pdf)
naturebank-filotis, a customization of NatureBank, which modifies the Django templates for the Filotis website hosting a database for the Greek nature.|[naturebank-filotis](https://github.com/ellak-monades-aristeias/naturebank-filotis)
An Ansible role that installs NatureBank on a server.|[naturebank-ansible](https://github.com/ellak-monades-aristeias/naturebank-ansible)
The database for the Natural Environment of Greece FILOTIS has been checked for compatibility with the CC-by-SA license, and WMS/WFS services have been established |[filotis](http://filotis.itia.ntua.gr/)
