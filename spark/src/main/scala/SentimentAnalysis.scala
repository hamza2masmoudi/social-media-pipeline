import org.apache.spark._
import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka010._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import edu.stanford.nlp.pipeline._
import edu.stanford.nlp.ling.CoreAnnotations
import java.util.Properties

object SentimentAnalysis {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("RealTimeSentimentAnalysis")
    val ssc = new StreamingContext(conf, Seconds(5))
    
    val kafkaParams = Map[String, Object](
      "bootstrap.servers" -> "localhost:9092",
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "spark-group",
      "auto.offset.reset" -> "latest"
    )
    
    val topics = Array("social-media")
    val stream = KafkaUtils.createDirectStream[String, String](
      ssc,
      LocationStrategies.PreferConsistent,
      ConsumerStrategies.Subscribe[String, String](topics, kafkaParams)
    )

    // NLP Pipeline
    def getSentiment(text: String): String = {
      val props = new Properties()
      props.setProperty("annotators", "tokenize, ssplit, parse, sentiment")
      val pipeline = new StanfordCoreNLP(props)
      val annotation = pipeline.process(text)
      val sentences = annotation.get(classOf[CoreAnnotations.SentencesAnnotation])
      sentences.get(0).get(classOf[CoreAnnotations.SentimentClass])
    }

    // Process stream
    stream.map(_.value)
      .foreachRDD { rdd =>
        val spark = SparkSession.builder.config(rdd.sparkContext.getConf).getOrCreate()
        import spark.implicits._
        
        val df = rdd.toDF("text")
        val getSentimentUDF = udf(getSentiment _)
        val results = df.withColumn("sentiment", getSentimentUDF($"text"))
        
        // Save to HDFS
        results.write
          .mode("append")
          .parquet("hdfs://localhost:9000/data/outputs/sentiment_results")
      }

    ssc.start()
    ssc.awaitTermination()
  }
}