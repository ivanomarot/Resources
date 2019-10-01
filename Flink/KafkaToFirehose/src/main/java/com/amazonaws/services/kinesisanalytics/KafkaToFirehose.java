package com.amazonaws.services.kinesisanalytics;

import com.amazonaws.services.kinesisanalytics.flink.connectors.config.ProducerConfigConstants;
import com.amazonaws.services.kinesisanalytics.flink.connectors.producer.FlinkKinesisFirehoseProducer;
import com.amazonaws.services.kinesisanalytics.runtime.KinesisAnalyticsRuntime;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer011;
import org.apache.flink.streaming.connectors.kinesis.FlinkKinesisConsumer;
import org.apache.flink.streaming.connectors.kinesis.FlinkKinesisProducer;
import org.apache.flink.streaming.connectors.kinesis.config.ConsumerConfigConstants;

import java.io.IOException;
import java.util.Map;
import java.util.Properties;

/**
 * A basic Kinesis Data Analytics for Java application with Kafa data
 * as source and Kinesis Firehose as a sink.
 */
public class KafkaToFirehose {
    private static final String region = "us-east-1";
    private static final String outputStreamName = "FirehoseEarthquakeStream";
    private static final String kafkaBootstrapServers = "b-1.ivan-kafka-sbox.dfyozz.c2.kafka.us-east-1.amazonaws.com:9092,b-2.ivan-kafka-sbox.dfyozz.c2.kafka.us-east-1.amazonaws.com:9092,b-3.ivan-kafka-sbox.dfyozz.c2.kafka.us-east-1.amazonaws.com:9092";
    private static final String kafkaZookeeperConnect = "10.9.10.228:2181,10.9.11.242:2181,10.9.9.251:2181";
    private static final String kafkaConsumerGroupId = "test";
    private static final String kafkaTopic = "earthquake-poc";

    private static DataStream<String> createKafkaSourceFromStaticConfig(StreamExecutionEnvironment env) {
        Properties inputProperties = new Properties();
        inputProperties.setProperty("bootstrap.servers", kafkaBootstrapServers);
        inputProperties.setProperty("zookeeper.connect", kafkaZookeeperConnect);
        inputProperties.setProperty("group.id", kafkaConsumerGroupId);

        return env.addSource(new FlinkKafkaConsumer011<>(kafkaTopic, new SimpleStringSchema(), inputProperties));
    }

    private static DataStream<String> createKafkaSourceFromApplicationProperties(StreamExecutionEnvironment env) throws IOException {
        Map<String, Properties> applicationProperties = KinesisAnalyticsRuntime.getApplicationProperties();
        return env.addSource(new FlinkKafkaConsumer011<>(kafkaTopic, new SimpleStringSchema(), applicationProperties.get("ConsumerConfigProperties")));
    }

    private static FlinkKinesisFirehoseProducer<String> createFirehoseSinkFromStaticConfig() {
        /*
         * com.amazonaws.services.kinesisanalytics.flink.connectors.config.ProducerConfigConstants
         * lists of all of the properties that firehose sink can be configured with.
         */

        Properties outputProperties = new Properties();
        outputProperties.setProperty(ConsumerConfigConstants.AWS_REGION, region);

        FlinkKinesisFirehoseProducer<String> sink = new FlinkKinesisFirehoseProducer<>(outputStreamName, new SimpleStringSchema(), outputProperties);
        ProducerConfigConstants config = new ProducerConfigConstants();
        return sink;
    }

    private static FlinkKinesisFirehoseProducer<String> createFirehoseSinkFromApplicationProperties() throws IOException {
        /*
         * com.amazonaws.services.kinesisanalytics.flink.connectors.config.ProducerConfigConstants
         * lists of all of the properties that firehose sink can be configured with.
         */

        Map<String, Properties> applicationProperties = KinesisAnalyticsRuntime.getApplicationProperties();
        FlinkKinesisFirehoseProducer<String> sink = new FlinkKinesisFirehoseProducer<>(outputStreamName, new SimpleStringSchema(), applicationProperties.get("ProducerConfigProperties"));
        return sink;
    }

    public static void main(String[] args) throws Exception {
        /* 
         * set up the streaming execution environment
         */
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        /* if you would like to use runtime configuration properties, uncomment the lines below
         * DataStream<String> input = createKafkaSourceFromApplicationProperties(env);
         */
        DataStream<String> input = createKafkaSourceFromStaticConfig(env);

        /* if you would like to use runtime configuration properties, uncomment the lines below
         * input.addSink(createFirehoseSinkFromApplicationProperties())
         */
        input.addSink(createFirehoseSinkFromStaticConfig());

        env.execute("Kafka consumer to Firehose sink");
    }
}
