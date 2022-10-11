# FaqApp

MVP webapp for telma.tv
Used for test and internal launch

## Pre-requesites

You must install

* `Python 3`: The app will use it to compile and run itself

* `PostgreSQL`: An open-source SQL database

Then, clone the repository:

```bash
$ git clone ....
```

The app is built under the **Django Framework** and **Django Rest Framework**.
An expertise with this tool is mandatory.

### Build & Run

Edit your configuration profile to set up your port, database connexion etc

```
$ cd telma-tv-my
nano src/main/resources/application.yml
```

Installing the package may suit some users

```bash
$ cd telma-tv-my
telma-tv-my$ mvn clean package -DskipTests
```

## Usage

`telma-tv-my` is an MVP (Minimum Valuable Product) to handle account management for Telma TV.

To run the app you need to:

```
telma-tv-my$ mvn spring-boot:run
```

or

```
telma-tv-my$ mvn spring-boot:run -Dspring-boot.run.profiles=foo,bar
```


