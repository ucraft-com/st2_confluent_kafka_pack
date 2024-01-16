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

1. Clone the st2_confluent_kafka_pack project into the designated StackStorm packs folder (/opt/stackstorm/packs):

```bash
git clone git@github.com:ucraft-com/st2_confluent_kafka_pack.git
```

2. Enter the pack folder
```bash
cd st2_confluent_kafka_pack/
```

3. Copy configuration example to stackstorm configs folder

```bash
cp st2_confluent_kafka_pack.example.yaml /opt/stackstorm/configs/st2_confluent_kafka_pack.yaml
```

4. Using editor (vim, nano) and fill in the form with your credentials

5. Install the pack

```bash
st2 pack install file://$PWD
```
