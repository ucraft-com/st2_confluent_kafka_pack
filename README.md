# UC StackStorm Kafka Sensor README

## Installation

Access the terminal and navigate to the /opt/stackstorm/packs/ directory. 

```bash
cd /opt/stackstorm/packs/
```

If you installed stackstorm in a different location, navigate to the stackstorm packs directory and continue the installation.

```bash
cd <STACKSTORM_PATH>/packs/
```

1. Clone the uc_kafka_sensor project into the designated StackStorm packs folder (/opt/stackstorm/packs):

```bash
git clone git@github.com:ucraft-com/uc_kafka_sensor.git
```

2. Enter the pack folder
```bash
cd uc_kafka_sensor/
```

3. Copy configuration example to stackstorm configs folder

```bash
cp uc_kafka_sensor.example.yaml /opt/stackstorm/configs/uc_kafka_sensor.yaml
```

4. Using editor (vim, nano) and fill in the form with your credentials

5. Install the pack

```bash
st2 pack install file://$PWD
```
