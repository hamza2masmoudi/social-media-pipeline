name := "RealTimeSentimentAnalysis"
version := "1.0"
scalaVersion := "2.12.15"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "3.3.0",
  "org.apache.spark" %% "spark-streaming" % "3.3.0",
  "org.apache.spark" %% "spark-sql" % "3.3.0",
  "org.apache.spark" %% "spark-streaming-kafka-0-10" % "3.3.0",
  "edu.stanford.nlp" % "stanford-corenlp" % "4.5.0",
  "edu.stanford.nlp" % "stanford-corenlp" % "4.5.0" classifier "models"
)